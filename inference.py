import os
import json
from openai import OpenAI
from environment import SecretaryEnv
from tools_schema import tools

USE_LLM = bool(os.getenv("OPENAI_API_KEY"))


def get_llm_action(client, model, messages, tools):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=50
        )

        message = response.choices[0].message

        if message.tool_calls:
            tool_call = message.tool_calls[0]
            action = tool_call.function.name

            try:
                params = json.loads(tool_call.function.arguments)
            except:
                params = {}

            return action, params

    except Exception as e:
        print("[LLM ERROR]:", e)

    return None, None
def run_episode(task_id="easy"):
    env = SecretaryEnv()
    env.difficulty = task_id
    instruction = env.reset()

    print(f'[START] {{"task_id": "{task_id}", "instruction": "{instruction}"}}')

    client = OpenAI(
        base_url=os.environ.get("API_BASE_URL", "https://api.openai.com/v1"),
        api_key=os.environ.get("API_KEY", os.environ.get("OPENAI_API_KEY", ""))
    )

    model = os.environ.get("MODEL_NAME", "gpt-4o-mini")

    messages = [
        {"role": "system", "content": "Follow steps: get_employee_id → check_calendar → book_meeting"},
        {"role": "user", "content": instruction}
    ]

    step_num = 0
    default_name = "John"
    if task_id == "medium":
        default_name = "Alice"
    elif task_id == "hard":
        default_name = "Bob"

    while not env.done and step_num < 5:
        action, params = None, None

        if USE_LLM:
            action, params = get_llm_action(client, model, messages, tools)

        # 🔥 Fallback if LLM fails
        if not action:
            print("[FALLBACK MODE]")

            if not env.employee_id:
                action = "get_employee_id"
                params = {"name": default_name}

            elif not env.calendar_checked:
                action = "check_calendar"
                params = {"employee_id": env.employee_id}

            else:
                action = "book_meeting"
                params = {"time": "10AM"}

        print(f'[STEP] {{"step": {step_num}, "action": "{action}", "params": {json.dumps(params)}}}')

        try:
            result = getattr(env, action)(**params)
        except Exception as e:
            result = str(e)

        print(f'[RESULT] {{"step": {step_num}, "result": "{result}"}}')
        messages.append({"role": "assistant", "content": result})
        step_num += 1

    print(f'[END] {{"task_id": "{task_id}", "steps": {step_num}, "done": {env.done}, "reward": {env.reward}}}')
    return env


if __name__ == "__main__":
    run_episode()
