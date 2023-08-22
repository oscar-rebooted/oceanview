![20240801 Project screenshot](https://github.com/user-attachments/assets/fd79f9ba-15ce-4666-bf5a-03494d241fe2)

**What is this repo**

A dashboard for visualising ships in real time, i.e., their current location and true heading, using aisstream.io

https://github.com/aisstream

**Purpose of this project**

This is only the 2nd web "app" that I build so was mainly a tool/source of motivation for me to explore technologies I'm curious about 

All around, am super happy I did it - great success!

![3d80a358135368fd36431d4e930b1c11](https://github.com/user-attachments/assets/9f8cb6b8-cf5f-41f2-985a-04745615aab4)


**What I learnt/gained exposure to through this project**
- Asynchronous functions for querying
- Pooling database connections
- Pydantic
- Querying a 3rd party API and processing its data, specifically a Websocket
- PostgreSQL/using pgadmin4
- FastAPI
- Docker & containerisation
- AWS: Lambda, RDS, IAM (basic), Cloudwatch
- Hosting on the cloud (looked into Heroku, Fly.io)

**What I would do if I had more time**
- Processing more messages from AISstreams e.g. ShipStaticData which includes ETA
- Showing TrueHeading=Null on frontend, not just =0
- Make the frontend using React
- Make the ship icons clickable so that you can see info about them
- Start storing location data of specific ships over time
- Make ML model to using historical data to improve upon ETA forecasts
- Authentication to access /ships api
- Interface where you can select which ships you want to see, rather than just taking ships in an area
- Implement Apache Kafka to learn more about streaming
- Set up a CI/CD pipeline
- Provision my infra with Terraform 
