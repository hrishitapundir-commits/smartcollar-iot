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

# temporary in-memory database
database = []

@app.post("/ingest-data")
def ingest_data(data: CattleData):
    database.append(data.dict())
    return {"status": "success", "received": data.dict()}

@app.get("/data")
def get_all_data():
    return {"count": len(database), "data": database}