import streamlit as st
import requests
import pandas as pd
from streamlit_autorefresh import st_autorefresh    

# Auto-refresh every 10 seconds
st_autorefresh(interval=5000, key="autofresh")

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

# Sidebar - Recent Alerts
with st.sidebar:
    st.header(" Recent Alerts")
    if alerts:
        for alert in alerts[:5]:
            st.warning(f"**{alert['device_id']}** - {alert['temperature']}°C at {alert['timestamp']}")
    else:
        st.success("No active alerts!")       

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
    df.columns = ["Device ID", "Temperature (°C)", "Heart Rate", "Activity", "Battery %", "Last Updated"]

    def color_battery(val):
        if val > 50:
            color = "green"
        elif val >= 20:
            color = "orange"
        else:
            color = "red"
        return f"color: {color}"
    styled_df = df.style.map(color_battery, subset=["Battery %"])
    st.dataframe(styled_df, use_container_width=True)

else:
    st.warning("No data available. Make sure the backend is running.")

# Temperature chart per cattle
st.subheader("Temperature History")

def fetch_cattle_data(device_id):
    try:
        response = requests.get(f"{API_URL}/cattle/{device_id}")
        return response.json()["data"]
    except:
        return[]
    
if summary:
    for cattle in summary:
        device_id = cattle["device_id"]
        data = fetch_cattle_data(device_id)
        if data:
            df_temp = pd.DataFrame(data)[["timestamp", "temperature"]]
            df_temp = df_temp.sort_values("timestamp")
            st.write(f"**{device_id}**")
            st.line_chart(df_temp.set_index("timestamp")["temperature"])

# Alerts section
st.subheader(" Recent Fever Alerts")

if alerts: 
    df_alerts = pd.DataFrame(alerts[:10])[["device_id", "timestamp", "temperature", "message"]]
    df_alerts.columns = ["Device ID", "Timestamp", "Temperature(°C)", "Message"]
    st.dataframe(df_alerts, use_container_width=True)
else:
    st.success("No active alerts!")
                                        
# Individual cattle view
st.subheader(" Drill Down by Cattle")

if summary:
    device_ids = [c["device_id"] for c in summary]
    selected = st.selectbox("Select a Cattle ID", device_ids)

    data = fetch_cattle_data(selected)

    if data:
        df_individual = pd.DataFrame(data)[["timestamp", "temperature"]]
        df_individual = df_individual.sort_values("timestamp")
        df_individual["fever_threshold"] = 40.0

        st.line_chart(df_individual.set_index("timestamp")[["temperature","fever_threshold"]]) 

