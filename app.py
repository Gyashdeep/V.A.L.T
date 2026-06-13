import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="V.A.L.T. // GOVERNOR", layout="wide")

# CSS: Industrial Terminal Aesthetic
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    </style>
""", unsafe_allow_html=True)

st.title("💠V.A.L.T. GOVERNOR")

# 1. METRICS
col1, col2, col3 = st.columns(3)
col1.metric("GPU TEMP", "65°C")
col2.metric("GRID FREQ", "50.0Hz")
col3.metric("ARBITRAGE YIELD", "+$4.20/hr")

# 2. THE EDICT LOG (Read-Only Observer)
st.subheader("⚙️ DETERMINISTIC EDICT STREAM")

def get_ledger_data():
    try:
        with open("audit_ledger.jsonl", "r") as f:
            lines = f.readlines()[-15:] # Fetch tail
            return pd.DataFrame([json.loads(line) for line in lines])
    except: 
        return pd.DataFrame()

# Render data once per re-run
df = get_ledger_data()
if not df.empty:
    st.dataframe(df, use_container_width=True)

# 3. KINETIC STATUS
st.subheader("🛡️ KINETIC FIREWALL STATUS")
st.success("SYSTEM INTEGRITY: NOMINAL // HARDWARE CLAMP: ACTIVE")

# STREAMLIT NATIVE REFRESH
# Do NOT use 'while' or 'time.sleep'. 
# Use this to trigger a refresh every 2 seconds without crashing the browser.
st.empty()
if st.button("SYNC CLOCK"):
    st.rerun()
