# smartcollar-iot
#  Smart Cattle Collar Monitoring System

A real-time IoT-based livestock health monitoring system that simulates sensor data from cattle collars and displays live health metrics on a web dashboard.

##  Live Demo
- **API:** https://web-production-9816e7.up.railway.app/docs
- **Dashboard:** (Streamlit Cloud link — add after deployment)

##  Tech Stack
- **Backend:** Python, FastAPI, Pydantic
- **Database:** MongoDB
- **Dashboard:** Streamlit
- **Deployment:** Railway (API), Streamlit Cloud (Dashboard)
- **Tools:** Git, GitHub, python-dotenv

##  Project Structure
smartcollar-iot/

├── backend/          # FastAPI backend with 5 REST endpoints

├── simulator/        # IoT data simulator with argparse

├── dashboard/        # Streamlit live dashboard

├── docs/             # API documentation and project logs

├── Procfile          # Railway deployment config

└── requirements.txt  # Python dependencies
##  Features
- Simulates real-time sensor data (temperature, heart rate, GPS, activity) for multiple cattle
- REST API with 5 endpoints for data ingestion, retrieval, alerts, and summaries
- Automatic fever detection — flags readings above 40°C and stores alerts separately
- MongoDB aggregation pipeline for efficient latest-reading-per-cattle queries
- Live Streamlit dashboard with auto-refresh, GPS map, temperature charts, and color-coded battery levels
- Deployed backend accessible via public URL

##  API Endpoints
| Endpoint | Method | Description |
|---|---|---|
| `/ingest-data` | POST | Receive and store sensor data |
| `/data` | GET | Last 50 readings |
| `/cattle/{device_id}` | GET | History for one cattle |
| `/alerts` | GET | All fever alerts |
| `/summary` | GET | Latest reading per cattle |

##  Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/hrishitapundir-commits/smartcollar-iot.git
cd smartcollar-iot
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add .env file** 
MONGO_URI=mongodb://localhost:27017/smartcollar
**5. Run backend**
```bash
uvicorn backend.backend:app --reload
```

**6. Run simulator**
```bash
python simulator/data_simulator.py --cows 3 --interval 2
```

**7. Run dashboard**
```bash
streamlit run dashboard/app.py
```
