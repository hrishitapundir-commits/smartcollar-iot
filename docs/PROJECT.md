# Smart Cattle Collar — Project Log

## Day 1-3
- Set up virtual environment and installed dependencies
- Created folder structure: /simulator, /backend, /dashboard, /docs
- Built data simulator with GPS, activity, argparse support
- Connected simulator to FastAPI backend via HTTP POST
- Added retry logic to simulator

## Day 4-5
- Added activity, latitude, longitude to CattleData model
- Added GET /data?limit=N endpoint
- Added GET /cattle/{device_id} endpoint
- Documented all endpoints in API.md
- Fixed activity field bug in backend

## Next Steps
- Connect MongoDB Atlas for permanent storage
- Add fever alert logic
- Build Streamlit dashboard

## Phase 2 - Backend + MongoDB (Day 6-10)
- Connected FastAPI backend to local MongoDB
- Two collections: cattle_readings and alerts
- Implemented fever alert logic (temperature > 40.0°C)
- Added 5 REST API endpoints: /ingest-data, /data, /cattle/{id}, /alerts, /summary
- Used MongoDB aggregation pipeline for /summary endpoint
- Added comments to all backend routes
- Secured  credentials using .env file
