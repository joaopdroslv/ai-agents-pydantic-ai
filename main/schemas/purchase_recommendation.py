from typing import List, Optional

from pydantic import BaseModel


class UserContext(BaseModel):
    name: str
    last_purchased: Optional[List[str]] = None


class PurchaseRecommendation(BaseModel):
    recommendation: str
    topic: str
