from env import SecretaryEnv
from llm_agent import LLMAgent
from tools_schema import tools


def run():
    env = SecretaryEnv()
    agent = LLMAgent()

    instruction = env.reset()

    messages = [
        {"role": "system", "content": "Call tools step by step"},
        {"role": "user", "content": instruction}
    ]

    logs = []

    while not env.done:
        action, params = agent.get_action(messages, tools)

        if not action and env.calendar_checked:
            action = "book_meeting"
            params = {}

        result = getattr(env, action)(**params)

        logs.append({
            "action": action,
            "result": result
        })

        messages.append({
            "role": "tool",
            "name": action,
            "content": result
        })

    return {
        "reward": env.reward,
        "steps": logs
    }