from typing import Dict

from pydantic_ai import Agent, ModelRetry

from main.models.local_qwen import local_qwen
from main.schemas.coupon_search import FoundCoupon

coupons_db: Dict[str, str] = {
    "BLACKFRIDAY": "25% OFF",
    "CHRISTIMAS10": "10% OFF",
}

coupon_agent = Agent(
    model=local_qwen,
    output_type=FoundCoupon,
    retries=2,
    system_prompt=(
        "U are an AI agent that returns discount coupons info in JSON format. "
        "If the coupon is not found, u should try to match the coupon code.\n"
        "For example, if BLACKFREIDAY does not exist, try BLACKFRIDAY.\n\n"
        "Response format: {'coupon': ..., 'description': ...}"
    ),
)


@coupon_agent.tool_plain
def search_coupon(coupon: str):
    description = coupons_db.get(coupon)

    if description is None:
        raise ModelRetry(
            f"Coupon '{coupon}' no found. "
            "Please check the spelling of the coupon and try again with the correct code!"
        )

    return description


question = "I want to use the coupon BLACKFRID"  # Typo error

answer = coupon_agent.run_sync(question)

print(answer.output.model_dump_json(indent=4))
