import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="V.A.L.T. // GOVERNOR", layout="wide")

# ... (Keep your CSS style block here) ...

st.title("💠V.A.L.T. GOVERNOR")

# Use a container for the Edict Stream
st.subheader("⚙️ DETERMINISTIC EDICT STREAM")
edict_container = st.empty() 

def load_data():
    try:
        # Read from the ledger
        data = []
        with open("audit_ledger.jsonl", "r") as f:
            # Get the last 10 lines
            lines = f.readlines()[-10:]
            for line in lines:
                data.append(json.loads(line))
        return pd.DataFrame(data)
    except: return pd.DataFrame()

# Infinite loop protection: Use st.rerun() only on user intent or a timer
while True:
    df = load_data()
    if not df.empty:
        # Use the container to update content instead of clearing the whole page
        with edict_container.container():
            st.dataframe(df, use_container_width=True)
    
    time.sleep(1) # Refresh rate of the dashboard
    st.rerun()
