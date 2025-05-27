from pydantic import BaseModel


class FoundCoupon(BaseModel):
    coupon: str
    description: str
