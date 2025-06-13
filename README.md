# 🧠 Pydantic AI Learning Project

This project is designed to explore and learn the core functionalities of **Pydantic**, focusing on its use within **AI-driven applications**, particularly those involving **agents, data validation**, and **structured responses** powered by LLMs (Large Language Models).

## 📦 Project Structure

```
main/
    │
    ├── agents/ # LLM agent examples using Pydantic validation
    ├── evals/ # Scripts for evaluating agent performance and responses
    ├── examples/ # Practical usage examples for agents and tools
    ├── models/ # Configuration of language models (e.g., Qwen via OpenAIModel)
    ├── schemas/ # Reusable schemas for structured responses
    ├── tools/ # Helper utilities used across agents
```

## 🚀 Features Explored

- 🧪 **Model abstraction using OpenAI-compatible providers (e.g., Qwen via Ollama)**
- 🧰 **Input/output validation using Pydantic**
- 🔗 **Agent chaining and context passing**
- 💬 **Conversation history handling**
- 🛠️ **Tool usage**
- 🌐 **External tool usage (e.g., DuckDuckGo search)**
- 🧠 **Structured answers and SQL generation with schema enforcement**

## 🐳 Running with Docker

Build and run everything

```bash
docker compose up --build  -d
```
