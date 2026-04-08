from env import SecretaryEnv
from llm_agent import LLMAgent
from tools_schema import tools

env = SecretaryEnv()
agent = LLMAgent()

instruction = env.reset()

messages = [
    {"role": "system", "content": "You must call tools step by step to schedule meeting."},
    {"role": "user", "content": instruction}
]

print("TASK:", instruction)

while not env.done:
    action, params = agent.get_action(messages, tools)

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