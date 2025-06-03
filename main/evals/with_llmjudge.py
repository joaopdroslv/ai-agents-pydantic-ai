from typing import Any

from pydantic_ai import Agent, format_as_xml
from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import IsInstance, LLMJudge

from main.models.local_qwen import local_qwen
from main.schemas.recipe import *

recipe_agent = Agent(
    local_qwen,
    output_type=Recipe,
    system_prompt=(
        "You are a helpful chef AI. Given a dish and dietary restriction, "
        "output a recipe in the following JSON format:\n\n"
        "{\n"
        '  "ingredients": ["..."],\n'
        '  "steps": ["..."]\n'
        "}\n\n"
        "Make sure the recipe follows the dietary restriction and is valid JSON."
    ),
    retries=3,
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


report = recipe_dataset.evaluate_sync(
    transform_recipe,
    max_concurrency=1,  # Evaluating one at a time because of poor PC capabilities
)

report.print(
    width=None,  # Uses the full width of the terminal
    baseline=None,  # No comparison baseline report
    include_input=True,  # Displays the inputs used in the test
    include_metadata=True,  # Displays metadata for each test case
    include_expected_output=True,  # Displays the expected output (if defined)
    include_output=True,  # Displays the model's actual output
    include_durations=True,  # Shows duration per test case
    include_total_duration=True,  # Shows total evaluation duration
    include_removed_cases=True,  # Displays removed or skipped cases
    include_averages=True,  # Displays average scores at the end
    input_config=None,  # Configuration for rendering input values (default)
    metadata_config=None,  # Configuration for displaying metadata
    output_config=None,  # Configuration for rendering output values
    score_configs=None,  # Custom rendering for numeric scores
    label_configs=None,  # Custom rendering for labels
    metric_configs=None,  # Custom rendering for aggregated metrics
    duration_config=None,  # Custom rendering for durations
)
