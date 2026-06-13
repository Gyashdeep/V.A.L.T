\import streamlit as st
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

# We define the expected return type here
agent = Agent(
    model=GroqModel('llama-3.3-70b-versatile'),
    system_prompt="You are V.A.L.T. Governor. Always respond in valid JSON matching the ValtetEdict schema."
)

# 3. GOVERNANCE ENGINE
def run_governance_cycle():
    telemetry = {"temp": 45.0, "hz": 50.0, "price": -2.5}
    try:
        # We use a simple prompt. We will parse the output manually to ensure compatibility.
        result = agent.run_sync(f"Current Stats: {telemetry}. Provide ValtetEdict JSON.")
        
        # Manual parsing of the output string into your model
        # This bypasses the 'result_type' keyword argument completely.
        import json
        import re
        
        # Extract JSON from the output string using regex
        json_match = re.search(r'\{.*\}', result.output, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
            edict = ValtetEdict(**data)
            
            entry = {
                "ts": pd.Timestamp.now().strftime("%H:%M:%S"), 
                "action": edict.action, 
                "reasoning": edict.reasoning
            }
            st.session_state.ledger.append(entry)
        else:
            st.error("Governor failed to produce valid JSON output.")
            
    except Exception as e:
        st.error(f"Governor Fault: {str(e)}")

# 4. UI
st.title("💠 V.A.L.T. SOVEREIGN TERMINAL")
if 'ledger' not in st.session_state: st.session_state.ledger = []

if st.button("EXECUTE GOVERNANCE CYCLE"):
    run_governance_cycle()

if st.session_state.ledger:
    st.dataframe(pd.DataFrame(st.session_state.ledger), use_container_width=True)
