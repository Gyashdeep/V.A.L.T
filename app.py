import streamlit as st
import pandas as pd
import json
import time

st.set_page_config(page_title="V.A.L.T. // GOVERNOR", layout="wide")

st.markdown("<style>.stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }</style>", unsafe_allow_html=True)

st.title("💠V.A.L.T. GOVERNOR")

# Create a placeholder for the live data
data_placeholder = st.empty()

def get_ledger_data():
    try:
        with open("audit_ledger.jsonl", "r") as f:
            lines = f.readlines()[-15:]
            return pd.DataFrame([json.loads(line) for line in lines])
    except: return pd.DataFrame()

# This loop updates the placeholder WITHOUT refreshing the whole page
# This stops the browser from "running infinitely"
while True:
    df = get_ledger_data()
    with data_placeholder.container():
        st.subheader("⚙️ DETERMINISTIC EDICT STREAM")
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.write("WAITING FOR SOVEREIGN EDICT...")
    
    time.sleep(2) # Polling interval (Controls how fast it updates)
