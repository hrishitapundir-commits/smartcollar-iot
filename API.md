# Smart Cattle Collar - API Documentation

## Base URL
http://127.0.0.1:8000

---

## Endpoints

### 1. POST /ingest-data
Receives sensor data from the cattle collar simulator.

**Request Body:**
```json
{
    "timestamp": "2026-05-11 20:00:00",
    "device_id": "CATTLE_001",
    "temperature": 38.5,
    "heart_rate": 72,
    "movement": "low",
    "activity": "grazing",
    "battery_level": 85,
    "latitude": 23.001,
    "longitude": 72.501
}
```

---

### 2. GET /data?limit=50
Returns the last N records from the database.

**Query Parameter:** 'limit' (default: 50)

---

### 3. GET /cattle/{device_id}
Returns all records for a specific cattle ID.

**Example** '/cattle/CATTLE_001'