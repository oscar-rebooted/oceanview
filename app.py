# rewrite and simplify so it doesn't use as many packages or fastAPI

from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
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

# When running locally, the frontend and backend are on different ports, so we need to allow cross-origin requests
# This allows all methods & headers but only for these specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"], # localhost is where the frontend is running in browser, and 127.0.0.1 is IP of the uvicorn server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
def index():
    with open("index.html", "r") as file:
        content = file.read()
        content = content.replace("GOOGLE_MAPS_API_KEY", os.getenv("GOOGLE_MAPS_API_KEY"))
    return HTMLResponse(content=content)