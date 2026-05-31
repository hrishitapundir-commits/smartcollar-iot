import streamlit as st
import requests
import pandas as pd

# Backend API URL
API_URL = "http://127.0.0.1:8000"

# Page config
st.set_page_config(page_title="Smart Cattle Monitor", layout="wide")
st.title(" Smart Cattle Monitoring Dashboard")

# Fetch summary data from backend
def fetch_summary():
    try:
        response = requests.get(f"{API_URL}/summary")
        return response.json()["summary"]
    except:
        return[]
    
# Fetch alerts from backend 
def fetch_alerts():
    try:
        response = requests.get(f"{API_URL}/alerts")
        return response.json()["alerts"]
    except:
        return[]

# Load data
summary = fetch_summary()
alerts = fetch_alerts()

# Metrics cards at the top
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Cattle", len(summary))

with col2:
    st.metric("Active Alerts", len(alerts))

with col3:
    if summary:
        avg_temp = round(sum(c["temperature"] for c in summary) / len(summary), 2)
        st.metric("Avg Temperature (°C)", avg_temp)
    else:
        st.metric("Avg Temperature (°C)", "N/A")

#Cattle data table
st.subheader("Latest Readings per Cattle")

if summary:
    df = pd.DataFrame(summary)[["device_id", "temperature", "heart_rate", "activity", "battery_level", "timestamp"]]
    df.columns = ["Device ID", "Temperature(°C)", "Heart Rate", "Activity", "Battery %", "Last Updated"]
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No data available. Make sure the backend is running.")
