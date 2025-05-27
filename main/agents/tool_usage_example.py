from pydantic_ai import Agent, Tool

from main.models.local_qwen import local_qwen
from main.schemas.product_price import ProductPrice
from main.tools.get_product_price import get_product_price

agent_tools = Agent(
    model=local_qwen,
    output_type=ProductPrice,
    system_prompt=(
        "You are a price search assistant. "
        "You can use the 'get_product_price' tool to help. "
        "Always return in JSON format with 'product' and 'price'. "
        "If the product's price is not available, price should be an empty string."
    ),
    tools=[Tool(function=get_product_price, takes_ctx=True)],
)

# question = "What is the price of an coconut (the fruit)?"
# > It should return an empty price, as the product does not exist in the database
# > {"product": "coconut", "price": ""}

question = "I want to buy a orange, what is it price?"
# > {"product": "orange", "price": "3.99"}

answer = agent_tools.run_sync(question)

print(answer.output.model_dump_json(indent=4))
