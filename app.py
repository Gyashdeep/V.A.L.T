import streamlit as st
import pandas as pd
import json
import time

st.set_page_config(page_title="V.A.L.T. // GOVERNOR", layout="wide")

# CSS: Industrial Terminal Aesthetic
st.markdown("<style>.stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }</style>", unsafe_allow_html=True)

st.title("💠V.A.L.T. GOVERNOR")

def get_ledger_data():
    try:
        # Check if file exists to prevent errors
        with open("audit_ledger.jsonl", "r") as f:
            lines = f.readlines()[-15:]
            return pd.DataFrame([json.loads(line) for line in lines])
    except: 
        return pd.DataFrame()

# RENDER SECTION
st.subheader("⚙️ DETERMINISTIC EDICT STREAM")
df = get_ledger_data()

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.write("WAITING FOR SOVEREIGN EDICT...")

# The "Sovereign" Refresh trigger
# This tells Streamlit to wait 2 seconds and then run the script again 
# naturally, rather than forcing an infinite 'while' loop.
time.sleep(2)
st.rerun()
