from pydantic import BaseModel


class ProductPrice(BaseModel):
    product: str
    price: str
