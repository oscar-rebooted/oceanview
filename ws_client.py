import asyncio
import websockets
import json
from dotenv import load_dotenv
import os
from pydantic import BaseModel
import asyncpg

load_dotenv()
api_key_aisstream = os.getenv('API_KEY_AISSTREAM')

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

class AISMessage(BaseModel):
    Message: dict
    MessageType: str
    MetaData: dict

class Ship(BaseModel):
    MMSI: int
    Latitude: float
    Longitude: float
    TrueHeading: int

db_conn = None

async def get_db_connection():
    global db_conn
    if db_conn is None or db_conn.is_closed():
        db_conn = await asyncpg.connect(user=DB_USER, password=DB_PASSWORD,
                                        database=DB_NAME, host=DB_HOST, port=DB_PORT)
    return db_conn

async def insert_ship(ship_instance, conn):
    async with conn.transaction():
        try:
            await conn.execute('''
                INSERT INTO ship_location(mmsi, latitude, longitude, trueheading) VALUES($1, $2, $3, $4)
                ON CONFLICT (MMSI) DO UPDATE
                SET latitude = EXCLUDED.latitude,
                    longitude = EXCLUDED.longitude,
                    trueheading = EXCLUDED.trueheading;
            ''', ship_instance.MMSI, ship_instance.Latitude, ship_instance.Longitude, ship_instance.TrueHeading)
        except Exception as e:
            print(f'Error: {e}')
            raise e

async def connect_aisstream():
    max_messages = 2
    message_count = 0

    conn = await get_db_connection()

    try: 
        async with websockets.connect('wss://stream.aisstream.io/v0/stream') as websocket:
            print('WebSocket connection established successfully')

            # English channel
            subscribe_message = {'APIKey': f'{api_key_aisstream}', 
                                'BoundingBoxes': [[[49.5, -1.5], [51, 1.7]]],
                                'FilterMessageTypes': ['PositionReport']}
            
            subscribe_message_json = json.dumps(subscribe_message)
            
            await websocket.send(subscribe_message_json)
            
            async for json_message in websocket:
                message_count += 1

                #Action code
                ais_message = AISMessage.model_validate_json(json_message)
                position_report = ais_message.Message['PositionReport']
                
                filtered_keys = ['UserID', 'Latitude', 'Longitude', 'TrueHeading']
                filtered_dict = {key: position_report[key] for key in filtered_keys}
                ship_instance = Ship(MMSI=filtered_dict['UserID'],
                                    Latitude=filtered_dict['Latitude'],
                                    Longitude=filtered_dict['Longitude'],
                                    TrueHeading=filtered_dict['TrueHeading'])
                
                await insert_ship(ship_instance, conn)

                if message_count >= max_messages:
                    await websocket.close()
                    break
    finally:
        await conn.close()        

if __name__ == '__main__':
    asyncio.run(connect_aisstream())