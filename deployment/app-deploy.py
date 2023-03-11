import os
from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List
from mangum import Mangum

DB_HOST = 'oceanview.cx40qca66kt5.eu-west-2.rds.amazonaws.com'
DB_PORT = '5432'
DB_NAME = 'ships'
DB_USER = 'oceanview_admin'
DB_PASSWORD = 'wzS1Fm79QaqJwban9Iir'

S3_BUCKET_URL = 'https://oceanview-exb5svq2.s3.eu-west-2.amazonaws.com'

app = FastAPI()

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

def fetch_ship_location():
    with get_db_connection() as conn:
        print("Success")
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT mmsi, latitude, longitude, trueheading FROM ship_location LIMIT 50")
            ship_records = cur.fetchall()
            ships = [Ship(MMSI=row["mmsi"], 
                        Latitude=row["latitude"],
                        Longitude=row["longitude"], 
                        TrueHeading=row["trueheading"] or 0) for row in ship_records] #TrueHeading can never be negative
    return ships

@app.get("/ships", response_model=List[Ship])
def get_ships():
    ships = fetch_ship_location()
    return ships

@app.get("/")
def index():
    return RedirectResponse(url=f'{S3_BUCKET_URL}/index.html')

handler = Mangum(app, lifespan='off')