from pydantic_ai import Agent

from main.models.local_qwen import local_qwen

agent = Agent(local_qwen)

message_history = None


def create_log(actor: str) -> str:
    from datetime import datetime

    now = datetime.now()
    return f"[CHAT] - [{now.date()} - {now.time().strftime('%H:%M:%S')}] - [{actor}]"


while True:
    user_input = input(f"\n{create_log("You")}: ")

    # Allow to end the conversation
    if user_input.lower() in ["exit", "quit"]:
        print(f"\n{create_log("System")}: Ending conversation with AI Agent.")
        break

    # If have a message history, send it
    result = agent.run_sync(user_input, message_history=message_history)

    print(f"\n{create_log("AI Agent")}: ", result.output)

    message_history = result.all_messages()
