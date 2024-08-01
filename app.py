# rewrite and simplify so it doesn't use as many packages or fastAPI

from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

S3_BUCKET_URL = os.getenv('S3_BUCKET_URL')

app = FastAPI()

origins = [
    S3_BUCKET_URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
) 

class Ship(BaseModel):
    MMSI: int
    Latitude: float
    Longitude: float
    TrueHeading: int

def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

max_ships_retrieved = 300

def fetch_ship_location():
    with get_db_connection() as conn:
        print("Success")
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(f"SELECT mmsi, latitude, longitude, trueheading FROM ship_location LIMIT {max_ships_retrieved}")
            ship_records = cur.fetchall()
            ships = [Ship(MMSI=row["mmsi"], 
                        Latitude=row["latitude"],
                        Longitude=row["longitude"], 
                        TrueHeading=row["trueheading"] or 0) for row in ship_records] #TrueHeading can never be negative
    return ships

@app.get("/ships", response_model=List[Ship])
async def get_ships():
    ships = fetch_ship_location()
    return ships

@app.get("/")
def index():
    return RedirectResponse(url=f'{S3_BUCKET_URL}/index.html')