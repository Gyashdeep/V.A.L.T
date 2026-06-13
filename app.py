import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="V.A.L.T. // GOVERNOR", layout="wide")
st.markdown("<style>.stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }</style>", unsafe_allow_html=True)

st.title("💠 PHASE-LOCK ZERO // V.A.L.T. GOVERNOR")
log_area = st.empty() # The container that prevents page flickering

def get_ledger():
    try:
        with open("audit_ledger.jsonl", "r") as f:
            lines = f.readlines()[-15:]
            return pd.DataFrame([json.loads(line) for line in lines])
    except: return pd.DataFrame()

# The UI Loop
while True:
    df = get_ledger()
    with log_area.container():
        st.subheader("⚙️ DETERMINISTIC EDICT STREAM")
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("SYSTEM INITIALIZING: WAITING FOR TELEMETRY...")
    
    # Simple refresh without forcing a page reload
    import time
    time.sleep(2)
