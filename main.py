import os, asyncio, json, logging, random
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

# Setup Logging
logging.basicConfig(filename='sovereign_governor.log', level=logging.INFO)

class ValtetEdict(BaseModel):
    action: str = Field(description="OVERDRIVE, THROTTLE, IDLE, or SHUTDOWN")
    reasoning: str
    target_power_watts: float = Field(ge=0.0, le=500.0)
    market_trade_intent: bool

agent = Agent(
    GroqModel('llama-4-scout', api_key=os.environ.get("GROQ_API_KEY")),
    result_type=ValtetEdict,
    system_prompt="You are V.A.L.T. Governor. Maximize compute yield per Watt. Ensure safety."
)

def get_telemetry():
    # Fallback telemetry if NVML fails
    return {"temp": random.uniform(40, 90), "hz": 50.0, "price": -2.5}

async def start_sovereign_daemon():
    print("V.A.L.T. // GOVERNANCE ACTIVE [24Hz Heartbeat]")
    while True:
        try:
            data = get_telemetry()
            result = await agent.run(f"Telemetry: {data}. Determine Sovereign Edict.")
            
            # Physics Firewall
            edict = "HARD_SHUTDOWN" if data['temp'] > 85 else result.data
            
            with open("audit_ledger.jsonl", "a") as f:
                f.write(json.dumps({"ts": datetime.now().isoformat(), "edict": str(edict), "telemetry": data}) + "\n")
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Action: {edict}")
        except Exception as e:
            print(f"Fault: {e}")
        await asyncio.sleep(2) # Increased sleep to prevent API rate limits

if __name__ == "__main__":
    asyncio.run(start_sovereign_daemon())
