from env import SecretaryEnv
from llm_agent import LLMAgent
from tools_schema import tools

env = SecretaryEnv()
agent = LLMAgent()

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
    action, params = agent.get_action(messages, tools)

    # force final step if LLM stops early
    if not action and env.calendar_checked:
        action = "book_meeting"
        params = {}

    if not action:
        print("No action returned")
        break

    print("\n[LLM ACTION]:", action, params)

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