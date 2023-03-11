from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import asyncpg
import asyncio
from typing import List

DB_HOST = 'oceanview.cx40qca66kt5.eu-west-2.rds.amazonaws.com'
DB_PORT = '5432'
DB_NAME = 'ships'
DB_USER = 'oceanview_admin'
DB_PASSWORD = 'wzS1Fm79QaqJwban9Iir'

app = FastAPI()

class Ship(BaseModel):
    MMSI: int
    Latitude: float
    Longitude: float
    TrueHeading: int

async def get_db_connection():
    return await asyncpg.connect(
        user=DB_USER, password=DB_PASSWORD,
        database=DB_NAME, host=DB_HOST, port=DB_PORT)

async def fetch_ship_location():
    conn = await get_db_connection()
    ship_records = await conn.fetch(
        "SELECT mmsi, latitude, longitude, trueheading FROM ship_location LIMIT 50"
    )
    ships = [Ship(MMSI=row["mmsi"], 
                Latitude=row["latitude"],
                Longitude=row["longitude"], 
                TrueHeading=row["trueheading"] or 0) for row in ship_records] #TrueHeading can never be negative
    await conn.close()
    return ships

@app.get("/ships", response_model=List[Ship])
async def get_ships():
    ships = await fetch_ship_location()
    return ships

app.mount('/static', StaticFiles(directory="public"), name="static")

@app.get("/")
async def index():
    return FileResponse(os.path.join(os.getcwd(), 'index.html'))