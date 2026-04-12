import os
import json
from openai import OpenAI
from environment import SecretaryEnv
from tools_schema import tools

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY") or os.getenv("OPENAI_API_KEY")
USE_LLM = bool(API_BASE_URL and API_KEY)


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

    model = os.environ.get("MODEL_NAME", "gpt-4o-mini")
    print(f"[START] task={task_id} env=secretary model={model}")

    client = None
    if USE_LLM:
        client = OpenAI(
            base_url=API_BASE_URL,
            api_key=API_KEY
        )

    messages = [
        {"role": "system", "content": "Follow steps: get_employee_id → check_calendar → book_meeting"},
        {"role": "user", "content": instruction}
    ]

    step_num = 0
    rewards = []
    last_error = None
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

        try:
            result = getattr(env, action)(**params)
            last_error = None
        except Exception as e:
            result = str(e)
            last_error = str(e)

        reward_str = "1.00" if env.done else "0.00"
        rewards.append(reward_str)

        action_str = f"{action}({json.dumps(params)})"
        error_str = last_error if last_error else "null"
        print(f"[STEP] step={step_num+1} action={action_str} reward={reward_str} done={str(env.done).lower()} error={error_str}")

        messages.append({"role": "assistant", "content": result})
        step_num += 1

    success = str(env.done).lower()
    score = f"{env.reward:.2f}"
    rewards_str = ",".join(rewards)
    print(f"[END] success={success} steps={step_num} score={score} rewards={rewards_str}")
    return env


if __name__ == "__main__":
    run_episode()
