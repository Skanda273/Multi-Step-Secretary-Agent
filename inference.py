import os
from openai import OpenAI
from env import SecretaryEnv

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(base_url=API_BASE_URL)


def run_episode(task=None):
    print("START")

    env = SecretaryEnv()
    instruction = env.reset()

    print("STEP reset", instruction)

    result = env.get_employee_id("John")
    print("STEP get_employee_id", result)

    result = env.check_calendar(env.employee_id)
    print("STEP check_calendar", result)

    result = env.book_meeting("10AM")
    print("STEP book_meeting", result)

    print("END", env.reward)

    return {
        "reward": env.reward
    }


if __name__ == "__main__":
    run_episode()