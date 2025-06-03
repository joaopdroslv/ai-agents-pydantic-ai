from pydantic import BaseModel


class CustomerOrder(BaseModel):
    dish_name: str
    dietary_restrition: str | None = None


class Recipe(BaseModel):
    ingredients: list[str]
    steps: list[str]
