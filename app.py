import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="V.A.L.T. TERMINAL", layout="wide")
st.markdown("<style>.stApp { background-color: #000; color: #00FF41; font-family: monospace; }</style>", unsafe_allow_html=True)

st.title("💠 V.A.L.T. SOVEREIGN TERMINAL")

# Placeholder for dynamic content
placeholder = st.empty()

def get_data():
    try:
        with open("audit_ledger.jsonl", "r") as f:
            return pd.DataFrame([json.loads(line) for line in f.readlines()[-10:]])
    except: return pd.DataFrame()

# Polling loop managed by Streamlit
while True:
    df = get_data()
    with placeholder.container():
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.write("SYSTEM INITIALIZING: WAITING FOR HEARTBEAT...")
    
    # Use standard time delay for UI refresh
    import time
    time.sleep(2)
    st.rerun()
