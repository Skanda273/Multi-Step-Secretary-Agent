from openai import OpenAI
import os
import time
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class LLMAgent:
    def get_action(self, messages, tools):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tools,
                tool_choice="auto",
                max_tokens=50
            )

            msg = response.choices[0].message

            if msg.tool_calls:
                tool_call = msg.tool_calls[0]
                return tool_call.function.name, eval(tool_call.function.arguments)

            return None, None

        except Exception as e:
            print("LLM ERROR:", e)
            time.sleep(1)
            return None, None