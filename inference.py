import os
import json
from env import SecretaryEnv
from llm_agent import LLMAgent
from tools_schema import tools

def run_episode(task_id="easy"):
    env = SecretaryEnv()
    env.difficulty = task_id
    instruction = env.reset()
    agent = LLMAgent()

    print(f'[START] {{"task_id": "{task_id}", "instruction": "{instruction}"}}')

    messages = [
        {"role": "system", "content": "You must call tools step by step to schedule a meeting."},
        {"role": "user", "content": instruction}
    ]

    step_num = 0

    while not env.done and step_num < 10:
        action, params = agent.get_action(messages, tools)

        if not action and env.calendar_checked:
            action = "book_meeting"
            params = {}

        if not action:
            break

        print(f'[STEP] {{"step": {step_num}, "action": "{action}", "params": {json.dumps(params)}}}')

        try:
            result = getattr(env, action)(**params)
        except Exception as e:
            result = str(e)

        messages.append({
            "role": "assistant",
            "content": json.dumps({"action": action, "params": params})
        })

        messages.append({
            "role": "tool",
            "name": action,
            "content": result
        })

        step_num += 1

    print(f'[END] {{"task_id": "{task_id}", "reward": {env.reward}, "done": {str(env.done).lower()}}}')

    return env.reward


if __name__ == "__main__":
    for task in ["easy", "medium", "hard"]:
        run_episode(task)
