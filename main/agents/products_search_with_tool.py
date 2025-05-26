from pydantic_ai import Agent, Tool, RunContext
from main.models.ollama_model import ollama_model
from main.schemas.product_details import Product, ProductSearchInput, ProductsExplained, FoundProducts
from main.products_db import products_db
from typing import List


agent_with_tool = Agent(
    model=ollama_model,
    input_type=ProductSearchInput,
    deps_type=FoundProducts,
    output_type=ProductsExplained,
    system_prompt=(
        "U are an agent specialized in searching for products, for this u must use "
        "your tool 'product_search_tool' which will receive the user's input and search the database "
        "for products that fits, your function after that is to take the list of products 'FoundProducts' "
        "that was returned by the tool, take the description of each the products and explain "
        "to the user the benefits that those features that the product has can provide."
        "Return the response in the format 'ProductsExplained'."
    ),
)


# Let's assume that "ProductSearchInput" comes from the frontend properly formatted
@agent_with_tool.tool
def product_search(ctx: RunContext, input: ProductSearchInput) -> FoundProducts:
    results = []

    # Could be replaced by a connection to a database and a query...
    for product in products_db.values():
        if input.name and input.name.lower() not in product.name.lower():
            continue

        if input.category and input.category.lower() != product.category.lower():
            continue

        if input.description_keywords:
            keywords = input.description_keywords.lower().split(",")
            if not all(keyword.strip() in product.description.lower() for keyword in keywords):
                continue

        if input.min_price and product.price < input.min_price:
            continue

        if input.max_price and product.price > input.max_price:
            continue

        results.append(product)

    return results


@agent_with_tool.system_prompt
async def inject_products(ctx: RunContext[FoundProducts]) -> str:
    products = ctx.deps

    # if not products:
    #     return "No products found."

    products_list = "\n".join(
        f"- Product(name='{p.name}', category='{p.category}', description='{p.description}', price='{p.price}')"
        for p in products
    )

    return (
        "You are an assistant that helps users understand the benefits of different electronic products.\n"
        "Here is a list of products found by the search tool:\n"
        f"{products_list}\n\n"
        "Your task is to explain the benefits of the features described for each product, "
        "and return a JSON object with the structure 'ProductsExplained'."
        "'ProductsExplained.found' represents the total amount of products found."
    )

search_input = ProductSearchInput(name="Iphone")

result = agent_with_tool.run_sync(search_input)

print(result)
