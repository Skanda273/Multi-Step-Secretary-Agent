import os
import json
from openai import OpenAI

class LLMAgent:
    def __init__(self):
        self.client = OpenAI(
            base_url=os.environ.get("API_BASE_URL", "https://api.openai.com/v1"),
            api_key=os.environ.get("API_KEY", os.environ.get("OPENAI_API_KEY", ""))
        )
        self.model = os.environ.get("MODEL_NAME", "gpt-4o-mini")

    def get_action(self, messages, tools):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )

            message = response.choices[0].message

            if message.tool_calls:
                tool_call = message.tool_calls[0]
                action = tool_call.function.name
                try:
                    params = json.loads(tool_call.function.arguments)
                except (json.JSONDecodeError, TypeError):
                    params = {}
                return action, params

            # If no tool call, try to parse action from text content
            content = message.content or ""
            if content:
                try:
                    data = json.loads(content)
                    return data.get("action"), data.get("params", {})
                except (json.JSONDecodeError, TypeError):
                    pass

            return None, None

        except Exception as e:
            print(f"[LLMAgent ERROR] {e}")
            return None, None
