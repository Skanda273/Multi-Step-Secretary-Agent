import os
import json
import sys
from openai import OpenAI
from environment import SecretaryEnv
from tools_schema import tools

def run_episode(task_id="easy"):
    env = SecretaryEnv()
    env.difficulty = task_id
    instruction = env.reset()

    client = OpenAI(
        base_url=os.environ.get("API_BASE_URL", "https://api.openai.com/v1"),
        api_key=os.environ.get("API_KEY", os.environ.get("OPENAI_API_KEY", ""))
    )
    model = os.environ.get("MODEL_NAME", "gpt-4o-mini")

    print(f'[START] {{"task_id": "{task_id}", "instruction": "{instruction}"}}')

    messages = [
        {"role": "system", "content": (
            "You are a secretary assistant. You must complete meeting scheduling tasks step by step "
            "using the provided tools. Always: 1) get_employee_id first, 2) check_calendar with the ID, "
            "3) book_meeting with an available time slot."
        )},
        {"role": "user", "content": instruction}
    ]

    step_num = 0

    while not env.done and step_num < 10:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
        except Exception as e:
            print(f"[ERROR] LLM call failed: {e}")
            break

        message = response.choices[0].message

        if not message.tool_calls:
            break

        tool_call = message.tool_calls[0]
        action = tool_call.function.name
        try:
            params = json.loads(tool_call.function.arguments)
        except (json.JSONDecodeError, TypeError):
            params = {}

        print(f'[STEP] {{"step": {step_num}, "action": "{action}", "params": {json.dumps(params)}}}')

        try:
            result = getattr(env, action)(**params)
        except Exception as e:
            result = str(e)

        messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": action,
                        "arguments": tool_call.function.arguments
                    }
                }
            ]
        })

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })

        step_num += 1

    # Return exactly the reward value
    score = float(env.reward)
    print(f'[END] {{"task_id": "{task_id}", "reward": {score:.2f}, "done": {str(env.done).lower()}}}')

    return score


if __name__ == "__main__":
    # If run as a script, only run the first task or follow command line arg
    tid = sys.argv[1] if len(sys.argv) > 1 else "easy"
    run_episode(tid)
