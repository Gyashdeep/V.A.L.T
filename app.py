import streamlit as st
import pandas as pd
import json
import time

st.set_page_config(page_title="V.A.L.T. // GOVERNOR", layout="wide")

st.markdown("<style>.stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }</style>", unsafe_allow_html=True)

st.title("💠V.A.L.T. GOVERNOR")

def get_ledger_data():
    try:
        with open("audit_ledger.jsonl", "r") as f:
            lines = f.readlines()[-15:]
            return pd.DataFrame([json.loads(line) for line in lines])
    except: 
        return pd.DataFrame()

# RENDER CONTENT
st.subheader("⚙️ DETERMINISTIC EDICT STREAM")
df = get_ledger_data()

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.write("WAITING FOR SOVEREIGN EDICT...")

# This is the "Heartbeat" - it tells Streamlit to wait 2 seconds 
# and then restart the script cleanly. No infinite 'while' loop needed.
time.sleep(2)
st.rerun()
