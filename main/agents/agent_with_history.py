import os
from datetime import datetime

import logfire
from dotenv import load_dotenv
from pydantic_ai import Agent

from main.models.local_qwen import local_qwen

load_dotenv()

# logfire.configure(token=os.getenv("LOGFIRE_TOKEN", None))
logfire.configure()  # Automatically get token from .env
logfire.instrument_pydantic_ai()

agent = Agent(local_qwen)

message_history = None


def create_log(actor: str) -> str:
    now = datetime.now()
    return f"[{now.date()} - {now.time().strftime('%H:%M:%S')}] [{actor}]"


while True:
    user_input = input(f"\n{create_log("You")}:\n\n ")

    # Allow to end the conversation
    if user_input.lower() in ["exit", "quit"]:
        print(f"\n{create_log("System")}:\n\n Ending conversation with AI Agent.")
        break

    # If have a message history, send it
    result = agent.run_sync(user_input, message_history=message_history)

    print(f"\n{create_log("AI Agent")}:\n\n ", result.output)

    message_history = result.all_messages()
