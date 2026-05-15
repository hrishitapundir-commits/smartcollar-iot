import random
import time
from datetime import datetime
import requests

API_URL = "http://127.0.0.1:8000/ingest-data"


def generate_data(device_id):
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "device_id": device_id,
        "temperature": round(random.uniform(37.0, 40.5), 2),
        "heart_rate": random.randint(60, 110),
        "movement": random.choice(["low", "medium", "high"]),
        "battery_level": random.randint(20, 100)
    }
    return data
    
if __name__ == "__main__":
    cattle_ids = ["CATTLE_001", "CATTLE_002", "CATTLE_003"]

    while True:
        for cid in cattle_ids:
            data = generate_data(cid)

            try:
                resp = requests.post(API_URL, json=data, timeout=5)
                print(f"Sent → {cid}: status={resp.status_code}")
            except Exception as e:
                print("Error sending data:", e)

        time.sleep(2)
