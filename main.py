import os
import asyncio
import json
import logging
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

# Ensure log exists
logging.basicConfig(filename='sovereign_governor.log', level=logging.INFO)

class ValtetEdict(BaseModel):
    action: str
    reasoning: str
    target_power_watts: float
    market_trade_intent: bool

agent = Agent(
    GroqModel('llama-3.3-70b-versatile', api_key=os.environ.get("GROQ_API_KEY")),
    result_type=ValtetEdict,
    system_prompt="You are V.A.L.T. Governor. Maximize yield. Maintain safety."
)

async def start_sovereign_daemon():
    print("V.A.L.T. // GOVERNANCE ACTIVE")
    while True:
        try:
            # Simulate Telemetry
            data = {"temp": 45.0, "hz": 50.0, "price": -2.5}
            
            # Agent Reasoning
            result = await agent.run("Determine optimal Sovereign Edict.")
            
            # Atomic Write
            with open("audit_ledger.jsonl", "a") as f:
                log = {"ts": datetime.now().isoformat(), "edict": result.data.model_dump(), "telemetry": data}
                f.write(json.dumps(log) + "\n")
                f.flush() # CRITICAL: Releases file for Dashboard to read
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Action Logged.")
        except Exception as e:
            logging.error(f"Governor Fault: {e}")
        
        await asyncio.sleep(5) # Increased sleep to prevent system overload

if __name__ == "__main__":
    asyncio.run(start_sovereign_daemon())
