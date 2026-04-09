import os
from openai import OpenAI

class LLMAgent:
    def __init__(self):
        self.client = OpenAI(
            base_url=os.environ["API_BASE_URL"],
            api_key=os.environ["API_KEY"]
        )

    def get_action(self, observation):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",  # or any model they allow
            messages=[
                {"role": "system", "content": "You are a helpful assistant that plans steps to schedule meetings."},
                {"role": "user", "content": observation}
            ]
        )

        return response.choices[0].message.content
