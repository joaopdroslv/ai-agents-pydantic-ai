from pydantic_ai import Agent
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool

from main.models.local_qwen import local_qwen

agent = Agent(
    model=local_qwen,
    tools=[duckduckgo_search_tool()],
    system_prompt="Search DuckDuckGo for the given query and return the results.",
)

question = (
    "Can u list the films that competed for the 2020 Oscar? "
    "Give me a brief summary, like a synopsis, of each of them."
)

answer = agent.run_sync(question)

print(answer.output)
