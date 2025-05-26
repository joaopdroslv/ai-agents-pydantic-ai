from pydantic import BaseModel
from typing import Optional, List

class Product(BaseModel):
    name: str
    category: str
    description: str  # Description entered in the database, from the person who registered the product
    price: float

class ProductSearchInput(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description_keywords: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None

class FoundProducts(BaseModel):
    products: List[Product]

class ProductExplained(BaseModel):
    name: str
    description: str
    price: float

class ProductsExplained(BaseModel):
    found: int
    products: Optional[List[ProductExplained]] = None
