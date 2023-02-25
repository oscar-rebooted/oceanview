from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict

load_dotenv()
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

# Not possible to have same script managing websocket connection and API endpoints
# Need to split the two and create a postgreSQL database

# Replace ships dictionary with data from postgresql
@app.get("/ships", response_model=Dict[int, Ship])
async def get_ships():
    return ships

app.mount('/static', StaticFiles(directory="public"), name="static")

@app.get("/")
async def index():
    return FileResponse(os.path.join(os.getcwd(), 'index.html'))
