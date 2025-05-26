from pydantic_ai import Agent, RunContext

from main.models.ollama_model import ollama_model
from main.schemas.purchase_recommendation import Recommendation, UserContext

most_purchased = [
    "Onyx Storm",
    "The Emperor of Gladness",
    "Heart Lamp: Selected Stories",
    "Mark Twain",
    "The Let Them Theory",
]

agent_with_context = Agent(
    model=ollama_model,
    output_type=Recommendation,
    deps_type=UserContext,
    system_prompt=(
        "U are a helper system for buyers, "
        "wich should recommend similar books, "
        "based on the topic, to those previously purchased by the user. "
        "If the user does not have previous purchases, "
        "recommend a book that are among the most purchased. "
        "Recommend only real and published books."
    ),
)


# Here we will change the default system prompt set
# to inject the user context
@agent_with_context.system_prompt
async def inject_last_purchases(context: RunContext[UserContext]) -> str:
    user_context = context.deps

    last_purchased = (
        f"User last purchases were: {', '.join(user_context.last_purchased)}."
        if user_context.last_purchased
        else "No previous purchases found. "
        f"These are the most purchased books for the moment: {', '.join(most_purchased)}"
    )

    return (
        f"User name: {user_context.name}. "
        f"{last_purchased} "
        "Always answer in JSON format, "
        " like {'recommendation': 'X' 'topic': 'Y'}. "
        "Recommendation is the name of the recommended book, and "
        "topic represents the type of book u detected the user has purchased "
        "recently, such as Sci-fi or Policital Science."
    )


# Simulating a user context to be passed
user_context = UserContext(
    name="Alexander",
    last_purchased=[
        "The Name of the Wind",
        "Mistborn: The Final Empire",
        "The Field Guide (from The Spiderwick Chronicles)",
    ],
)
# Likely to classify user tastes as "fantasy" and recommend a fantasy book

answer = agent_with_context.run_sync(
    user_prompt="I don't know wich book to buy...", deps=user_context
)

print(answer.output.model_dump_json(indent=4))
