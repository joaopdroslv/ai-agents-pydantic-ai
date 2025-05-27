from pydantic_ai import Agent

from main.models.local_qwen import local_qwen
from main.schemas.question_classification import QuestionClassification

scructured_agent = Agent(
    model=local_qwen,
    system_prompt=(
        "U are an agent whose objective is only to classify questions."
        "To each question, answer in JSON format."
        "Answer in 'pt-BR'."
        "The keys are: 'text' with represents your explanation of why that classification "
        "and 'difficult_level' with represents the difficult level "
        "u classified the question, from 0 to 10."
    ),
    output_type=QuestionClassification,
)

question = "Explain the difference between 'mais' and 'mas' in Brazilian Portuguese."

structured_answer = scructured_agent.run_sync(question)

print(structured_answer.output.model_dump_json(indent=4))
