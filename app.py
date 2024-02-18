import asyncio
import websockets
import json
from dotenv import load_dotenv
import os
from datetime import datetime, timezone

load_dotenv()
api_key = os.getenv('API_KEY')

async def connect_aistream():
    max_messages = 5
    message_count = 0

    async with websockets.connect('wss://stream.aisstream.io/v0/stream') as websocket:
        print('WebSocket connection established successfully')

        # English channel
        subscribe_message = {'APIKey': f'{api_key}', 
                            'BoundingBoxes': [[[49.5, -1.5], [51, 1.7]]],
                            'FilterMessageTypes': ['PositionReport']}
        
        subscribe_message_json = json.dumps(subscribe_message)
        
        await websocket.send(subscribe_message_json)

        async for json_message in websocket:
            message_count += 1
            ais_message = json.loads(json_message)
            
            #Action code
            print(ais_message)

            if message_count >= max_messages:
                await websocket.close()

if __name__ == '__main__':
    asyncio.run(connect_aistream())