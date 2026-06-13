import os
import asyncio
import json
import logging
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

# 1. SETUP: Logging and Telemetry
logging.basicConfig(filename='sovereign_governor.log', level=logging.INFO)

try:
    import nvidia_smi
    nvidia_smi.nvmlInit()
    HAS_GPU = True
except:
    HAS_GPU = False

class ValtetEdict(BaseModel):
    action: str = Field(description="OVERDRIVE, THROTTLE, IDLE, or SHUTDOWN")
    reasoning: str
    target_power_watts: float
    market_trade_intent: bool

# PIVOT: Switched to llama-3.3-70b-versatile
agent = Agent(
    GroqModel('llama-3.3-70b-versatile', api_key=os.environ.get("GROQ_API_KEY")),
    result_type=ValtetEdict,
    system_prompt="You are V.A.L.T. Governor. Maximize compute yield via grid arbitrage. Maintain safety."
)

def get_hardware_telemetry():
    if HAS_GPU:
        handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)
        temp = nvidia_smi.nvmlDeviceGetTemperature(handle, 0)
    else:
        temp = 45.0 # Fallback for non-GPU dev environments
    return {"temp": temp, "hz": 50.0, "price": -2.5}

def execute_edict(edict: ValtetEdict, telemetry: dict):
    # KINETIC FIREWALL: Hard-coded logic for physical protection
    if telemetry['temp'] > 85.0 or telemetry['hz'] < 49.5:
        return "HARD_SHUTDOWN"
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "decision": edict.model_dump(),
        "telemetry": telemetry
    }
    with open("audit_ledger.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    return "EXECUTED"

async def start_sovereign_daemon():
    print("V.A.L.T. // GOVERNANCE ACTIVE [Llama-3.3-70b Engine]")
    while True:
        try:
            data = get_hardware_telemetry()
            # Agent reasoning cycle
            result = await agent.run(f"Current Stats: {data}. Actuate.")
            status = execute_edict(result.data, data)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Action: {result.data.action} | Status: {status}")
        except Exception as e:
            logging.error(f"Governor Fault: {e}")
        
        await asyncio.sleep(2) # Stabilized heartbeat

if __name__ == "__main__":
    asyncio.run(start_sovereign_daemon())
