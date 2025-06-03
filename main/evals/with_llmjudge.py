from typing import Any

from pydantic_ai import Agent, format_as_xml
from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import IsInstance, LLMJudge

from main.models.local_qwen import local_qwen
from main.schemas.recipe import *

# What is LLMJudge?
#
# LLMJudge is an evaluator provided by the pydantic-evals library.
# It allows you to automatically evaluate the output of an LLM (Large Language Model)
# based on qualitative, subjective, or open-ended criteria.
#
# Rather than relying on strict rules or exact matching, LLMJudge leverages
# another LLM as the judge to assess whether a given output meets a certain rubric
# (set of evaluation instructions or goals).
#
# How does it work under the hood?
#
# It constructs a prompt like:
# “Given the input and output below, does the output satisfy the rubric: ‘[your rubric here]’?”
# Sends this prompt to a judge model (e.g., gpt-4, claude-3, etc.).
# Interprets the judge's response to decide whether the case passes.
#
# This makes it a powerful tool for evaluating tasks like:
# - Instruction following
# - Ethical alignment
# - Style and tone matching
# - Content filtering
# - Creative writing or summarization


recipe_agent = Agent(
    local_qwen,
    output_type=Recipe,
    system_prompt=(
        "You are a helpful chef AI. Given a dish and dietary restriction, output a recipe in the following JSON format:\n\n"
        "{\n"
        '  "ingredients": ["..."],\n'
        '  "steps": ["..."]\n'
        "}\n\n"
        "Make sure the recipe follows the dietary restriction and is valid JSON."
    ),
    retries=1,
)


async def transform_recipe(customer_order: CustomerOrder) -> Recipe:
    answer = await recipe_agent.run(format_as_xml(customer_order))
    return answer.output


recipe_dataset = Dataset[CustomerOrder, Recipe, Any](
    cases=[
        Case(
            name="vegetarian_recipe",
            inputs=CustomerOrder(
                dish_name="Spaghetti Bolognese", dietary_restriction="vegetarian"
            ),
            expected_output=None,
            metadata={"focus": "vegetarian"},
            evaluators=(
                LLMJudge(
                    rubric="Recipe should not contain meat or animal products",
                    model=local_qwen,
                ),
            ),
        ),
        Case(
            name="gluten_free_recipe",
            inputs=CustomerOrder(
                dish_name="Chocolate Cake", dietary_restriction="gluten-free"
            ),
            expected_output=None,
            metadata={"focus": "gluten-free"},
            evaluators=(
                LLMJudge(
                    rubric="Recipe should not contain gluten or wheat products",
                    model=local_qwen,
                ),
            ),
        ),
    ],
    evaluators=[
        IsInstance(type_name="Recipe"),
        LLMJudge(
            rubric="Recipe should have clear steps and relevant ingredients.",
            model=local_qwen,
        ),
    ],
)


report = recipe_dataset.evaluate_sync(transform_recipe)
print(report)
