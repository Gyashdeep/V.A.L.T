import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="V.A.L.T. TERMINAL", layout="wide")

# Static CSS
st.markdown("<style>.stApp { background-color: #000; color: #00FF41; }</style>", unsafe_allow_html=True)

st.title("💠 V.A.L.T. SOVEREIGN TERMINAL")

def get_ledger_data():
    try:
        # Atomic read: open and close immediately
        with open("audit_ledger.jsonl", "r") as f:
            lines = f.readlines()
            # Get last 15 lines safely
            data = [json.loads(line) for line in lines[-15:]]
            return pd.DataFrame(data)
    except:
        return pd.DataFrame()

# UI Layout
st.subheader("⚙️ DETERMINISTIC EDICT STREAM")

# Display data once per render
df = get_ledger_data()
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("Waiting for Governor output...")

# MANUAL REFRESH BUTTON
# This replaces time.sleep() and st.rerun() to stop the "infinite" feel.
# The user clicks this to see the latest data.
if st.button("REFRESH DATA"):
    st.rerun()
