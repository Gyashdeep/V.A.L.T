import streamlit as st
import pandas as pd
import os
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

# 1. SCHEMA
class ValtetEdict(BaseModel):
    action: str = Field(description="OVERDRIVE, THROTTLE, IDLE, or SHUTDOWN")
    reasoning: str
    target_power_watts: float
    market_trade_intent: bool

# 2. SETUP AGENT
api_key = st.secrets.get("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = api_key

agent: Agent[None, ValtetEdict] = Agent(
    GroqModel('llama-3.3-70b-versatile'),
    system_prompt="You are V.A.L.T. Governor. Maximize yield via grid arbitrage. Maintain safety."
)

# 3. GOVERNANCE ENGINE
def run_governance_cycle():
    telemetry = {"temp": 45.0, "hz": 50.0, "price": -2.5}
    try:
        result = agent.run_sync(f"Current Stats: {telemetry}. Actuate.")
        
        # FIX: Check if .data exists, otherwise use the result object directly
        # Some versions return the model object itself directly
        edict = getattr(result, 'data', result)
        
        entry = {
            "ts": pd.Timestamp.now().strftime("%H:%M:%S"), 
            "action": edict.action, 
            "reasoning": edict.reasoning
        }
        st.session_state.ledger.append(entry)
    except Exception as e:
        # Debugging: show exactly what the result object looks like if it fails
        st.error(f"Governor Fault: {str(e)}")
        st.write("Result object:", result)

# 4. UI
st.title("💠 V.A.L.T. SOVEREIGN TERMINAL")
if 'ledger' not in st.session_state: st.session_state.ledger = []

if st.button("EXECUTE GOVERNANCE CYCLE"):
    run_governance_cycle()

if st.session_state.ledger:
    st.dataframe(pd.DataFrame(st.session_state.ledger), use_container_width=True)
