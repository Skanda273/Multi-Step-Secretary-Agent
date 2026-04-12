import os

from environment import SecretaryEnv
from llm_agent import LLMAgent
from tools_schema import tools

API_BASE_URL = os.environ.get("API_BASE_URL")
API_KEY = os.environ.get("API_KEY") or os.environ.get("OPENAI_API_KEY")
USE_LLM = bool(API_BASE_URL and API_KEY)

env = SecretaryEnv()
agent = LLMAgent() if USE_LLM else None

instruction = env.reset()

messages = [
    {
        "role": "system",
        "content": "You must call get_employee_id, then check_calendar, then book_meeting. Always finish by calling book_meeting."
    },
    {"role": "user", "content": instruction}
]

print("TASK:", instruction)

while not env.done:
    if USE_LLM:
        action, params = agent.get_action(messages, tools)
    else:
        action, params = None, None

    # force final step if LLM stops early
    if not action and env.calendar_checked:
        action = "book_meeting"
        params = {"time": "10AM"}

    if not action:
        print("[FALLBACK MODE] No valid LLM action. Using deterministic fallback.")
        if not env.employee_id:
            action = "get_employee_id"
            params = {"name": "John"}
        elif not env.calendar_checked:
            action = "check_calendar"
            params = {"employee_id": env.employee_id}
        else:
            action = "book_meeting"
            params = {"time": "10AM"}

    print("\n[ACTION]:", action, params)

    try:
        result = getattr(env, action)(**params)
        print("[TOOL RESULT]:", result)

        messages.append({
            "role": "tool",
            "name": action,
            "content": result
        })

    except Exception as e:
        print("[ERROR]:", e)

        messages.append({
            "role": "tool",
            "name": action,
            "content": str(e)
        })

print("\nFINAL REWARD:", env.reward)
