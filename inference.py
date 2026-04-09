import os
import json
from openai import OpenAI
from env import SecretaryEnv
from tools_schema import tools

API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.environ.get("HF_TOKEN", "")

client = OpenAI(
    api_key=HF_TOKEN if HF_TOKEN else os.environ.get("OPENAI_API_KEY", ""),
    base_url=API_BASE_URL
)


def run_episode(task_id="easy"):
    env = SecretaryEnv()
    env.difficulty = task_id
    instruction = env.reset()

    print(f'[START] {{"task_id": "{task_id}", "instruction": "{instruction}"}}')

    messages = [
        {"role": "system", "content": "You must call tools step by step to schedule a meeting."},
        {"role": "user", "content": instruction}
    ]

    step_num = 0

    while not env.done and step_num < 10:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        msg = response.choices[0].message

        if not msg.tool_calls:
            break

        for tc in msg.tool_calls:
            action = tc.function.name
            params = json.loads(tc.function.arguments)

            print(f'[STEP] {{"step": {step_num}, "action": "{action}", "params": {json.dumps(params)}}}')

            try:
                result = getattr(env, action)(**params)
            except Exception as e:
                result = str(e)

            messages.append({
                "role": "assistant",
                "content": None,
                "tool_calls": [tc]
            })

            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result
            })

            step_num += 1

    print(f'[END] {{"task_id": "{task_id}", "reward": {env.reward}, "done": {str(env.done).lower()}}}')

    return env.reward


if __name__ == "__main__":
    for task in ["easy", "medium", "hard"]:
        run_episode(task)