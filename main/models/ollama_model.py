from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

ollama_model = OpenAIModel(
    model_name="qwen2.5:14b",
    provider=OpenAIProvider(base_url="http://localhost:11434/v1"),
)
