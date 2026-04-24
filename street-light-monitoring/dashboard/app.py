import streamlit as st
import pydeck as pdk
import pandas as pd
from ai_model.fault_detector import detect_fault, fault_severity
from utils.alert_system import generate_alert

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Street Light Monitoring",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("💡 Centralized Street Light Monitoring System")
st.caption("Smart city dashboard for AI-based street light fault detection")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/street_lights.csv")

# Ensure valid coordinates
df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
df = df.dropna(subset=["latitude", "longitude"])

# ---------------- FAULT DETECTION ----------------
df["fault"] = df.apply(detect_fault, axis=1)
df["severity"] = df["fault"].apply(fault_severity)

faulty_df = df[df["fault"] != "Normal"]
normal_df = df[df["fault"] == "Normal"]

# ---------------- METRICS ----------------
total = len(df)
faulty = len(faulty_df)
healthy = len(normal_df)

col1, col2, col3 = st.columns(3)
col1.metric("💡 Total Lights", total)
col2.metric("🔴 Faulty Lights", faulty)
col3.metric("🟢 Healthy Lights", healthy)

# ---------------- MAP (PYDECK) ----------------
st.subheader("🗺️ Street Light Status Map")
st.caption("🔴 Faulty | 🟡 Warning | 🟢 Healthy")

def map_color(row):
    if row["severity"] == "High":
        return [255, 0, 0]        # 🔴 Faulty
    elif row["severity"] == "Medium":
        return [255, 255, 0]      # 🟡 Warning
    else:
        return [0, 255, 0]        # 🟢 Healthy

df["color"] = df.apply(map_color, axis=1)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position="[longitude, latitude]",
    get_color="color",
    get_radius=90,
    pickable=True
)

view_state = pdk.ViewState(
    latitude=df["latitude"].mean(),
    longitude=df["longitude"].mean(),
    zoom=11
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={
        "text": "Light ID: {light_id}\nFault: {fault}\nSeverity: {severity}"
    }
)

st.pydeck_chart(deck)

# ---------------- FAULT TABLE ----------------
st.subheader("⚠️ Faulty Street Lights")

def highlight_fault(row):
    if row["severity"] == "High":
        return ["background-color:#7a2e2e; color:white"] * len(row)
    elif row["severity"] == "Medium":
        return ["background-color:#6b5e1d; color:black"] * len(row)
    else:
        return ["background-color:#14532d; color:white"] * len(row)

st.dataframe(
    faulty_df.style
        .apply(highlight_fault, axis=1)
        .set_properties(**{
            "border": "1px solid #374151",
            "text-align": "center"
        }),
    width="stretch"
)

# ---------------- ALERTS ----------------
st.subheader("🚨 Alerts")

for _, row in faulty_df.iterrows():
    if row["severity"] == "High":
        st.error(generate_alert(row["light_id"], row["fault"]))
    elif row["severity"] == "Medium":
        st.warning(generate_alert(row["light_id"], row["fault"]))
    else:
        st.info(generate_alert(row["light_id"], row["fault"]))

# ---------------- ANALYTICS ----------------
st.subheader("📊 Fault Analytics")
st.caption("Distribution of detected fault types")

fault_counts = df["fault"].value_counts()
st.bar_chart(fault_counts)
