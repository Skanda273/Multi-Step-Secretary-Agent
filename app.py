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

        result = getattr(env, action)(**params)
        output.append(f"[TOOL RESULT]: {result}")

        messages.append({
            "role": "tool",
            "name": action,
            "content": result
        })

    output.append(f"\nFINAL REWARD: {env.reward}")

    return "\n".join(output)


with gr.Blocks() as demo:
    gr.Markdown("# Multi Step Secretary Agent")
    btn = gr.Button("Run Agent")
    output = gr.Textbox(lines=20)
    btn.click(run_agent, outputs=output)

demo.launch()