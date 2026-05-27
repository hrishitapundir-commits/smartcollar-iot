from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

#MongoDB connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client["smartcollar"]
collection = db["cattle_readings"]

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

@app.post("/ingest-data")
def ingest_data(data: CattleData):
    record = data.dict()

    #Alert logic
    record["alert"] = False
    record["alert_reason"] = None

    if data.temperature > 39.5:
        record["alert"] = True
        record["alert_reason"] = f"High temperature: {data.temperature}°C"

    collection.insert_one(record)
    record.pop("_id", None)
    return {"status": "success", "received": record}    

@app.get("/data")
def get_all_data(limit: int = 50):
    records = list(collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit))
    return {"count": len(records), "data": records}

@app.get("/cattle/{device_id}")
def get_cattle_data(device_id: str):
    records = list(collection.find({"device_id": device_id}, {"_id": 0}))
    return {"device_id": device_id, "count": len(records), "data": records}

@app.get("/alerts")
def get_alerts():
    alerts = list(collection.find({"alert": True}, {"_id": 0}))
    return {"count": len(alerts), "alerts": alerts}
