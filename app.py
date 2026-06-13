import streamlit as st
import pandas as pd
import json
import time
from groq import Groq
from pydantic import BaseModel, Field
from datetime import datetime

# 1. SCHEMA & FIREWALL
class ValtetEdict(BaseModel):
    action: str = Field(description="OVERDRIVE, THROTTLE, IDLE, or SHUTDOWN")
    reasoning: str
    target_power_watts: float
    market_trade_intent: bool

def kinetic_firewall(temp: float, hz: float) -> bool:
    """Hard-coded physical safety override."""
    return temp < 85.0 and hz >= 49.5

# 2. SETUP
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

st.title("💠 V.A.L.T. SOVEREIGN TERMINAL")
if 'ledger' not in st.session_state: st.session_state.ledger = []

# 3. GOVERNANCE ENGINE (with Firewall)
def run_governance_cycle():
    # Simulating telemetry (In a real app, replace with sensor calls)
    telemetry = {"temp": 45.0, "hz": 50.0, "price": -2.5}
    
    prompt = f"Act on {telemetry}. Respond ONLY in JSON: {ValtetEdict.model_json_schema()['properties']}"
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        
        data = json.loads(response.choices[0].message.content)
        edict = ValtetEdict(**data)
        
        # APPLY KINETIC FIREWALL
        if not kinetic_firewall(telemetry['temp'], telemetry['hz']):
            edict.action = "HARD_SHUTDOWN"
            edict.reasoning = "FIREWALL VIOLATION: Thermal/Frequency limit exceeded."
        
        # IMMUTABLE LEDGERING
        entry = {"ts": datetime.now().strftime("%H:%M:%S"), "action": edict.action, "reasoning": edict.reasoning}
        st.session_state.ledger.append(entry)
        
        # FILE LOGGING
        with open("audit_ledger.jsonl", "a") as f:
            f.write(json.dumps(entry) + "\n")
            
    except Exception as e:
        st.error(f"Governor Fault: {str(e)}")

# 4. AUTO-REFRESH LOOP (The "Daemon" Feel)
if st.sidebar.button("ACTIVATE SOVEREIGN DAEMON"):
    while True:
        run_governance_cycle()
        st.rerun() # Forces the UI to update with the new ledger entry

st.dataframe(pd.DataFrame(st.session_state.ledger), use_container_width=True)
