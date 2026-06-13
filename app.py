import streamlit as st
import pandas as pd
import json
import time

st.set_page_config(page_title="V.A.L.T. // GOVERNOR", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    </style>
""", unsafe_allow_html=True)

st.title("💠 PHASE-LOCK ZERO // V.A.L.T. GOVERNOR")

# 1. METRICS (Hardcoded placeholder until you hook up live state)
col1, col2, col3 = st.columns(3)
with col1: st.metric("GPU TEMP", "65°C")
with col2: st.metric("GRID FREQ", "50.0Hz")
with col3: st.metric("ARBITRAGE YIELD", "+$4.20/hr")

# 2. THE EDICT LOG (Read-Only)
st.subheader("⚙️ DETERMINISTIC EDICT STREAM")

def get_ledger_data():
    try:
        with open("audit_ledger.jsonl", "r") as f:
            lines = f.readlines()[-15:] # Get last 15 entries
            return pd.DataFrame([json.loads(line) for line in lines])
    except: 
        return pd.DataFrame()

# Display the data frame once per render
df = get_ledger_data()
if not df.empty:
    st.dataframe(df, use_container_width=True)

# 3. KINETIC STATUS
st.subheader("🛡️ KINETIC FIREWALL STATUS")
st.success("SYSTEM INTEGRITY: NOMINAL // HARDWARE CLAMP: ACTIVE")

# REFRESH LOGIC: 
# Do NOT use 'while True'. Use this to refresh every 2 seconds.
time.sleep(2)
st.rerun()
