![20240801 Project screenshot](https://github.com/user-attachments/assets/fd79f9ba-15ce-4666-bf5a-03494d241fe2)

## What is this repo

A dashboard for visualising ships in real time, i.e., their current location and true heading, using aisstream.io

https://github.com/aisstream

Mainly a tool/source of motivation for me to explore technologies I'm curious about, namely:
- Websockets
- Asynchronous logic
- Managing database connections
- Pydantic
- PostgreSQL/using pgadmin4
- FastAPI
- Docker & containerisation
- AWS: Lambda, RDS, IAM (basic), Cloudwatch

## What I would do if I had more time
- Processing more messages from AISstreams e.g. ShipStaticData which includes ETA
- Showing TrueHeading=Null on frontend, not just =0
- Start storing location data of specific ships over time
- Make ML model to using historical data to improve upon ETA forecasts
- Authentication to access /ships api

## License
This project is licensed under the MIT License. However, it includes dependencies that are licensed under the LGPL-3.0, such as `psycopg2`. 