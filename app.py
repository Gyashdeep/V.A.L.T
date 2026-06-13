import streamlit as st
import pandas as pd
from pydantic import BaseModel, Field
from pydantic_ai import Agent

# 1. PAGE CONFIG
st.set_page_config(page_title="V.A.L.T. // GOVERNOR", layout="wide")
st.markdown("<style>.stApp { background-color: #000; color: #00FF41; font-family: monospace; }</style>", unsafe_allow_html=True)

# 2. SCHEMA
class ValtetEdict(BaseModel):
    action: str = Field(description="OVERDRIVE, THROTTLE, IDLE, or SHUTDOWN")
    reasoning: str
    target_power_watts: float
    market_trade_intent: bool

# 3. INITIALIZE AGENT
# Ensure GROQ_API_KEY is in Streamlit Cloud Settings > Secrets
api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY missing. Please configure it in Streamlit Cloud Settings -> Secrets.")
    st.stop()

# Initialize Agent using the string provider format
agent = Agent(
    'groq:llama-3.3-70b-versatile',
    api_key=api_key,
    result_type=ValtetEdict,
    system_prompt="You are V.A.L.T. Governor. Maximize yield via grid arbitrage. Maintain safety."
)

# 4. STATE MANAGEMENT
if 'ledger' not in st.session_state:
    st.session_state.ledger = []

# 5. GOVERNANCE ENGINE
def run_governance_cycle():
    telemetry = {"temp": 45.0, "hz": 50.0, "price": -2.5}
    try:
        result = agent.run_sync(f"Current Stats: {telemetry}. Actuate.")
        edict = result.data
        entry = {"ts": pd.Timestamp.now().strftime("%H:%M:%S"), "action": edict.action, "reasoning": edict.reasoning}
        st.session_state.ledger.append(entry)
    except Exception as e:
        st.error(f"Governor Fault: {str(e)}")

# 6. UI
st.title("💠 V.A.L.T. SOVEREIGN TERMINAL")

if st.button("EXECUTE GOVERNANCE CYCLE"):
    run_governance_cycle()

if st.session_state.ledger:
    st.dataframe(pd.DataFrame(st.session_state.ledger), use_container_width=True)
else:
    st.info("System Ready. Execute cycle to begin.")
