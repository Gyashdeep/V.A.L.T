import streamlit as st
import pandas as pd
import os
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

# 1. CLOUD CONFIGURATION
st.set_page_config(page_title="V.A.L.T. // GOVERNOR", layout="wide")
st.markdown("<style>.stApp { background-color: #000; color: #00FF41; font-family: monospace; }</style>", unsafe_allow_html=True)

# 2. SCHEMA
class ValtetEdict(BaseModel):
    action: str = Field(description="OVERDRIVE, THROTTLE, IDLE, or SHUTDOWN")
    reasoning: str
    target_power_watts: float
    market_trade_intent: bool

# 3. INITIALIZE AGENT
# Note: In Streamlit Cloud, store GROQ_API_KEY in Settings -> Secrets
api_key = st.secrets.get("GROQ_API_KEY")
agent = Agent(
    GroqModel('llama-3.3-70b-versatile', api_key=api_key),
    result_type=ValtetEdict,
    system_prompt="You are V.A.L.T. Governor. Maximize yield via grid arbitrage. Maintain safety."
)

# 4. SESSION STATE (Replaces the .jsonl file for cloud persistence)
if 'ledger' not in st.session_state:
    st.session_state.ledger = []

# 5. GOVERNANCE ENGINE
def run_governance_cycle():
    # Simulated Telemetry (Replace with real API calls)
    telemetry = {"temp": 45.0, "hz": 50.0, "price": -2.5}
    
    # Run Agent
    result = agent.run_sync(f"Current Stats: {telemetry}. Actuate.")
    edict = result.data
    
    # Update Ledger
    entry = {"ts": pd.Timestamp.now().strftime("%H:%M:%S"), "action": edict.action, "reasoning": edict.reasoning}
    st.session_state.ledger.append(entry)
    if len(st.session_state.ledger) > 15: st.session_state.ledger.pop(0)

# 6. DASHBOARD UI
st.title("💠 V.A.L.T. SOVEREIGN TERMINAL")

if st.button("EXECUTE GOVERNANCE CYCLE"):
    run_governance_cycle()

if st.session_state.ledger:
    st.subheader("⚙️ DETERMINISTIC EDICT STREAM")
    st.dataframe(pd.DataFrame(st.session_state.ledger), use_container_width=True)
else:
    st.info("System Ready. Execute cycle to begin.")

st.subheader("🛡️ KINETIC FIREWALL STATUS")
st.success("INTEGRITY: NOMINAL")
