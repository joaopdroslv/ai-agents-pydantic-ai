from pydantic_ai import Agent
from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import Evaluator, EvaluatorContext, IsInstance

from main.models.local_qwen import local_qwen

agent = Agent(
    local_qwen,
    system_prompt=(
        "Answer as directly as possible, for example:\n\n"
        "What is the capital of Brazil?\n\n"
        "Just answer: 'Federal District'"
    ),
)


class MatchAnswer(Evaluator[str, str]):
    def evaluate(self, ctx: EvaluatorContext[str, str]) -> float:
        if ctx.output == ctx.expected_output:
            return 1.0
        elif (
            isinstance(ctx.output, str)
            and ctx.expected_output.lower() in ctx.output.lower()
        ):
            return 0.8
        return 0.0


dataset = Dataset(
    cases=[
        Case(
            name="capital_question",
            inputs="What is the capital of France?",
            expected_output="Paris",
        ),
        Case(
            name="isaac_newton_born_city",
            inputs="In which place (village or town) was Isaac Newton born?",
            expected_output="Woolsthorpe",
        ),
        Case(
            name="uranium_235_atomic_number",
            inputs="What is the atomic number of Uranium-235?",
            expected_output="92",
        ),
    ],
    evaluators=[IsInstance(type_name="str"), MatchAnswer()],
)


async def answer_question(question: str) -> str:
    answer = await agent.run(question)
    return answer.output


report = dataset.evaluate_sync(answer_question)
report.print(include_input=True, include_output=True)
