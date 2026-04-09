from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from environment import SecretaryEnv

app = FastAPI(title="Multi-Step Secretary Agent", version="1.0.0")
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


@app.get("/health")
async def health():
    return {"status": "ok"}


dist_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "openenv-dashboard", "dist")
if os.path.exists(dist_path):
    app.mount("/", StaticFiles(directory=dist_path, html=True), name="static")


def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
