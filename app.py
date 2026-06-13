import streamlit as st
import pandas as pd
import json
from groq import Groq
from pydantic import BaseModel, Field

# 1. SCHEMA
class ValtetEdict(BaseModel):
    action: str = Field(description="OVERDRIVE, THROTTLE, IDLE, or SHUTDOWN")
    reasoning: str
    target_power_watts: float
    market_trade_intent: bool

# 2. SETUP CLIENT
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 3. GOVERNANCE ENGINE
def run_governance_cycle():
    # Current detected state
    telemetry = {"temp": "HIGH", "hz": 50.0, "price": -2.5}
    
    prompt = f"""You are V.A.L.T. Governor. Act on: {telemetry}. 
    Because the price is negative, prioritize consuming power unless temperature exceeds safety limits.
    Respond ONLY with a JSON object matching this schema: 
    {{"action": "str", "reasoning": "str", "target_power_watts": float, "market_trade_intent": bool}}"""
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        
        data = json.loads(response.choices[0].message.content)
        edict = ValtetEdict(**data)
        
        entry = {
            "ts": "06:11:20", 
            "action": edict.action, 
            "reasoning": edict.reasoning
        }
        st.session_state.ledger.append(entry)
            
    except Exception as e:
        st.error(f"Governor Fault: {str(e)}")

# 4. UI
st.title("💠 V.A.L.T. SOVEREIGN TERMINAL")
if 'ledger' not in st.session_state: 
    st.session_state.ledger = []

if st.button("EXECUTE GOVERNANCE CYCLE"):
    run_governance_cycle()

if st.session_state.ledger:
    st.dataframe(pd.DataFrame(st.session_state.ledger), use_container_width=True)
