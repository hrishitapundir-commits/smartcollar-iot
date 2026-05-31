from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from.env file
load_dotenv()

app = FastAPI()

# Connect to MongoDB using URI from . env
client = MongoClient(os.getenv("MONGO_URI"))
db = client["smartcollar"]

# Two collections - readings and alerts kept separate
collection = db["cattle_readings"]
alerts_collection = db["alerts"]

# Pydantic model - validates incoming data structure automatically
class CattleData(BaseModel):
    timestamp: str
    device_id: str
    temperature: float
    heart_rate: int
    movement: str
    activity: str
    battery_level: int
    latitude: float
    longitude: float

# POST /ingets-data - receives sensor data, checks for fever, stores in MongoDB
@app.post("/ingest-data")
def ingest_data(data: CattleData):
    record = data.dict()

    # Default: no alert
    record["alert"] = False
    record["alert_reason"] = None

    # Fever detection - normal cattle temp is 38-39.5°C, fever above 40°C
    if data.temperature > 40.0:
        record["alert"] = True
        record["alert_reason"] = f"High temperature: {data.temperature}°C"
        alerts_collection.insert_one({
            "device_id": data.device_id,
            "timestamp": data.timestamp,
            "temperature": data.temperature,
            "message": f"Fever alert: {data.temperature}°C"
        })

    collection.insert_one(record)
    record.pop("_id", None)  # Remove MongoDB's internal  _id before returning
    return {"status": "success", "received": record}    

# GET /data - returns last N readings (default 50), newest first
@app.get("/data")
def get_all_data(limit: int = 50):
    records = list(collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit))
    return {"count": len(records), "data": records}

# GET /cattle/{device_id} - returns full history for one specific cow
@app.get("/cattle/{device_id}")
def get_cattle_data(device_id: str):
    records = list(collection.find({"device_id": device_id}, {"_id": 0}))
    return {"device_id": device_id, "count": len(records), "data": records}

# GET /alerts - returns all fever alerts, newest first
@app.get("/alerts")
def get_alerts():
    alerts = list(alerts_collection.find({}, {"_id": 0}).sort("timestamp",-1))
    return {"count": len(alerts), "alerts": alerts}

# GET /summary - returns latest reading per cattle ID using aggregation pipeline
@app.get("/summary")
def get_summary():
    pipeline = [
        {"$sort": {"timestamp": -1}},       # Sort newest first
        {"$group": {                           # Group by cattle ID
            "_id": "$device_id",
            "latest": {"$first": "$$ROOT"}     # Take first (latest) record
        }},
        {"$replaceRoot": {"newRoot": "$latest"}}, # Make full record the output
        {"$project": {"_id": 0}}                  #  Hide _id field
    ]
    summary = list(collection.aggregate(pipeline))
    return {"count": len(summary), "summary": summary}
