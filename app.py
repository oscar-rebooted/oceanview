import asyncio
import websockets
import json
from dotenv import load_dotenv
import os
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict

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

ships = {}

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
            
            ships[ship_instance.MMSI] = ship_instance

            if message_count >= max_messages:
                await websocket.close()

# Not possible to have same script managing websocket connection and API endpoints
# Need to split the two and create a postgreSQL database
                
# if __name__ == '__main__':
#     asyncio.run(connect_aisstream())

@app.get("/ships", response_model=Dict[int, Ship])
async def get_ships():
    return ships

app.mount('/static', StaticFiles(directory="public"), name="static")

@app.get("/")
async def index():
    return FileResponse(os.path.join(os.getcwd(), 'index.html'))
