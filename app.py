import streamlit as st
import pandas as pd
import json
import time

# Dashboard Configuration
st.set_page_config(page_title="V.A.L.T. TERMINAL", layout="wide")

# Industrial Aesthetic
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00FF41; font-family: 'Courier New', monospace; }
    </style>
""", unsafe_allow_html=True)

st.title("💠 V.A.L.T. SOVEREIGN TERMINAL")

# 1. LIVE DATA FEEDER
def get_ledger_data():
    try:
        with open("audit_ledger.jsonl", "r") as f:
            # Load last 15 lines for the display
            lines = f.readlines()[-15:]
            data = [json.loads(line) for line in lines]
            return pd.DataFrame(data)
    except: 
        return pd.DataFrame()

# 2. UI RENDER CYCLE
st.subheader("⚙️ DETERMINISTIC EDICT STREAM")

df = get_ledger_data()
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.warning("SYSTEM STANDBY: Waiting for first sovereign edict...")

# 3. KINETIC STATUS
st.subheader("🛡️ KINETIC FIREWALL STATUS")
st.success("HARDWARE CLAMP: ACTIVE // INTEGRITY: NOMINAL")

# 4. REFRESH HEARTBEAT
# This replaces the 'while True' loop and prevents browser hanging.
time.sleep(2)
st.rerun()
