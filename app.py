import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="V.A.L.T. TERMINAL", layout="wide")
st.markdown("<style>.stApp { background-color: #000; color: #00FF41; font-family: monospace; }</style>", unsafe_allow_html=True)

st.title("💠 V.A.L.T. SOVEREIGN TERMINAL")

def get_ledger_data():
    try:
        with open("audit_ledger.jsonl", "r") as f:
            lines = f.readlines()
            return pd.DataFrame([json.loads(line) for line in lines[-10:]])
    except: return pd.DataFrame()

# Static Display
st.subheader("⚙️ DETERMINISTIC EDICT STREAM")
df = get_ledger_data()

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.write("WAITING FOR SOVEREIGN EDICT...")

# This button is the ONLY way to refresh the data
if st.button("SYNC DATA"):
    st.rerun()
