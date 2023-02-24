import asyncio
import websockets
import json
from dotenv import load_dotenv
import os
from datetime import datetime, timezone
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()
api_key_aisstream = os.getenv('API_KEY')

app = FastAPI()

class AISMessage(BaseModel):
    Message: dict
    MessageType: str
    MetaData: dict

class Ship(BaseModel):
    MMSI: int
    Latitude: float
    Longitude: float
    TrueHeading: int

async def connect_aisstream():
    max_messages = 2
    message_count = 0

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
            
            # Add ship_instance to a database

            if message_count >= max_messages:
                await websocket.close()

if __name__ == '__main__':
    asyncio.run(connect_aisstream())