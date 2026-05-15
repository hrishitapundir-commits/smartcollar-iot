from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CattleData(BaseModel):
    timestamp: str
    device_id: str
    temperature: float
    heart_rate: int
    movement: str
    battery_level: int
    latitude: float
    longitude: float

# temporary in-memory database
database = []

@app.post("/ingest-data")
def ingest_data(data: CattleData):
    database.append(data.dict())
    return {"status": "success", "received": data.dict()}

@app.get("/data")
def get_all_data(limit: int = 50):
    return {"count": len(database[-limit:]), "data": database[-limit:]}

@app.get("/cattle/{device_id}")
def get_cattle_data(device_id: str):
    cattle_records = [d for d in database if f["device_id"] == device_id]
    return{"device_id": device_id, "count": len(cattle_records), "data": cattle_records}