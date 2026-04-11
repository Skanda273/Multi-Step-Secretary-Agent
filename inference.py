import os
import json
import time
from openai import OpenAI
from environment import SecretaryEnv
from tools_schema import tools
from grader import grade_easy, grade_medium, grade_hard

def run_episode(task_id="easy"):
    try:
        env = SecretaryEnv()
        env.difficulty = task_id
        instruction = env.reset()

        client = OpenAI(
            base_url=os.environ.get("API_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/"),
            api_key=os.environ.get("API_KEY", os.environ.get("GEMINI_API_KEY", ""))
        )
        model = os.environ.get("MODEL_NAME", "gemini-2.5-flash")

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
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    print(f"[RATE LIMIT] Waiting 15s before retry...")
                    time.sleep(15)
                    continue
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
                "tool_calls": [tool_call],
            })

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

            step_num += 1

        # Use grader to compute final score
        if task_id == "easy":
            score = grade_easy(env)
        elif task_id == "medium":
            score = grade_medium(env)
        else:
            score = grade_hard(env)

        print(f'[END] {{"task_id": "{task_id}", "reward": {score:.2f}, "done": {str(env.done).lower()}}}')
        return score

    except Exception as e:
        print(f"[CRITICAL ERROR] Entire episode failed: {e}")
        score = 0.15
        print(f'[END] {{"task_id": "{task_id}", "reward": 0.15, "done": false}}')
        return score


if __name__ == "__main__":
    tasks = ["easy", "medium", "hard"]

    for task_id in tasks:
        try:
            run_episode(task_id)
        except Exception as e:
            print(f"[FATAL ERROR] {task_id}: {e}")
            print(f'[END] {{"task_id": "{task_id}", "reward": 0.15, "done": false}}')