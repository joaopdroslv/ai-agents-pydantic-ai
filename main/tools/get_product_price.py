from typing import Dict

from pydantic_ai import RunContext

products_db: Dict[str, float] = {
    "banana": 2.57,
    "apple": 3.11,
    "orange": 3.99,
}


def get_product_price(ctx: RunContext, product: str) -> str:
    price = products_db.get(product.lower())

    if price is None:
        return f"There is no price information for '{product.lower()}'."

    return f"{product} price is ${price:.2f}."
