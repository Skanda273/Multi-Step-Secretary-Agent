import gradio as gr
from env import SecretaryEnv
from llm_agent import LLMAgent
from tools_schema import tools


def run_agent():
    env = SecretaryEnv()
    agent = LLMAgent()

    instruction = env.reset()

    messages = [
        {
            "role": "system",
            "content": "You must call get_employee_id, then check_calendar, then book_meeting."
        },
        {"role": "user", "content": instruction}
    ]

    output = []
    output.append(f"TASK: {instruction}")

    while not env.done:
        action, params = agent.get_action(messages, tools)

        if not action and env.calendar_checked:
            action = "book_meeting"
            params = {}

        if not action:
            break

        output.append(f"\n[LLM ACTION]: {action} {params}")

        try:
            result = getattr(env, action)(**params)
            output.append(f"[TOOL RESULT]: {result}")

            messages.append({
                "role": "tool",
                "name": action,
                "content": result
            })

        except Exception as e:
            output.append(f"[ERROR]: {e}")

    output.append(f"\nFINAL REWARD: {env.reward}")

    return "\n".join(output)


demo = gr.Interface(
    fn=run_agent,
    inputs=[],
    outputs="text",
    title="Multi Step Secretary Agent",
    description="LLM tool calling meeting scheduler"
)

demo.launch(server_name="0.0.0.0", server_port=7860)