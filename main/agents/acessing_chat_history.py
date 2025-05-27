import asyncio

from pydantic_ai import Agent

from main.models.local_qwen import local_qwen

agent = Agent(model=local_qwen, system_prompt="Be a helpful assistant.")

question1 = "Tell me a joke."

# Simple way to see all messages of the stream
# answer = agent.run_sync(question1)
# print(answer.output)
# print("\n")
# print(answer.all_messages())


async def main():
    async with agent.run_stream(question1) as answer:

        # Incomplete messages before the stream finishes
        async for text in answer.stream_text():
            print("\n")
            print(text)

        print("\n")
        print(answer.all_messages())


asyncio.run(main())
