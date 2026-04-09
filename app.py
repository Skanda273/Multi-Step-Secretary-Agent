from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
import os

from env import SecretaryEnv

app = FastAPI()
env = SecretaryEnv()

class ActionRequest(BaseModel):
    action: str
    params: Dict[str, Any] = {}

@app.post("/reset")
async def reset():
    obs = env.reset()
    return {"observation": obs, "info": {}}

@app.post("/step")
async def step(req: ActionRequest):
    try:
        obs = getattr(env, req.action)(**req.params)
        return {
            "observation": obs,
            "reward": env.reward,
            "done": env.done,
            "info": {}
        }
    except Exception as e:
        return {
            "error": str(e),
            "observation": str(e),
            "reward": env.reward,
            "done": env.done,
            "info": {}
        }

@app.get("/state")
async def state():
    return {
        "employee_id": env.employee_id,
        "available_slots": env.available_slots,
        "calendar_checked": env.calendar_checked,
        "reward": env.reward,
        "done": env.done,
        "difficulty": env.difficulty
    }

if os.path.exists("openenv-dashboard/dist"):
    app.mount("/", StaticFiles(directory="openenv-dashboard/dist", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)