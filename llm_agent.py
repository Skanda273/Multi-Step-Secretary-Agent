import os
import json
from openai import OpenAI

class LLMAgent:
    def __init__(self):
        self.api_base_url = os.environ.get("API_BASE_URL")
        self.api_key = os.environ.get("API_KEY") or os.environ.get("OPENAI_API_KEY")

        if not self.api_base_url or not self.api_key:
            print("[LLMAgent WARNING] Missing API_BASE_URL or API_KEY. LLM calls will be disabled.")
            self.client = None
        else:
            self.client = OpenAI(
                base_url=self.api_base_url,
                api_key=self.api_key
            )

        self.model = os.environ.get("MODEL_NAME", "gpt-4o-mini")

    def get_action(self, messages, tools):
        if not self.client:
            return None, None

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
