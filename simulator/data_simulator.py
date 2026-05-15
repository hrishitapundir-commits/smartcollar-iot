import random
import time
from datetime import datetime
import requests
import argparse

API_URL = "http://127.0.0.1:8000/ingest-data"


def generate_data(device_id):
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "device_id": device_id,
        "temperature": round(random.uniform(37.0, 40.5), 2),
        "heart_rate": random.randint(60, 110),
        "movement": random.choice(["low", "medium", "high"]),
        "activity": random.choice(["grazing", "walking", "idle"]),
        "battery_level": random.randint(20, 100),
        "latitude": round(random.uniform(23.00, 23.05), 6),
        "longitude": round(random.uniform(72.50, 72.55), 6)
    }
    return data
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cattle Data Simulator")
    parser.add_argument("--cows", type=int, default=3, help="Number of cows to simulate")
    parser.add_argument("--interval", type=int, default=2, help="Seconds between each send")
    args = parser.parse_args()

    cattle_ids = [f"CATTLE_{str(i+1).zfill(3)}" for i in range(args.cows)]

    print(f"Simulating {args.cows} cows every {args.interval} seconds...")

    while True:
        for cid in cattle_ids:
            data = generate_data(cid)
            for attempt in range(3):
                try:
                    resp = requests.post(API_URL, json=data, timeout=5)
                    print(f"Sent → {cid}: status={resp.status_code}")
                    break
                except Exception as e:
                    print(f"Attempt {attempt+1} failed: {e}. Retrying in 3 seconds...")
                    time.sleep(3)
        time.sleep(args.interval)





