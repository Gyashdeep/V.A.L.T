import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="V.A.L.T. TERMINAL", layout="wide")

st.markdown("<style>.stApp { background-color: #000; color: #00FF41; font-family: 'Courier New', monospace; }</style>", unsafe_allow_html=True)

st.title("💠 V.A.L.T. SOVEREIGN TERMINAL")

def get_ledger_data():
    try:
        with open("audit_ledger.jsonl", "r") as f:
            lines = f.readlines()
            # Get the last 15 entries
            data = [json.loads(line) for line in lines[-15:]]
            return pd.DataFrame(data)
    except:
        return pd.DataFrame()

st.subheader("⚙️ DETERMINISTIC EDICT STREAM")

# Display the data once. No loops, no reruns.
df = get_ledger_data()
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("System Standby: No ledger data found. Check if main.py is writing to audit_ledger.jsonl")

# Add a manual trigger if needed, but remove st.rerun()
if st.button("SYNC WITH GOVERNOR"):
    st.rerun()
