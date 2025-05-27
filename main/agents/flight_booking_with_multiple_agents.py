import datetime
import logging
import os
from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.messages import ModelMessage
from pydantic_ai.usage import Usage, UsageLimits
from rich.prompt import Prompt

from main.models.local_qwen import local_qwen

# ===== Logging Configuration ===== #

LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../logs"))
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "info.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)

# ===================================


class FlightDetails(BaseModel):
    flight_number: str
    price: int
    origin: str = Field(description="Three-letter airport code.")
    destination: str = Field(description="Three-letter airport code.")
    date: datetime.date


class NoFlightFound(BaseModel):
    """When no valid flights is found."""


@dataclass
class Deps:
    web_page_text: str
    req_origin: str
    req_destination: str
    req_date: datetime.date


# This agent is responsible for controlling the flow of the conversation
search_agent = Agent(
    model=local_qwen,
    output_type=FlightDetails | NoFlightFound,
    retries=4,
    system_prompt="Ur job is to find the cheapest flight for the user on the diven date.",
)


# This agente is responsible for extracting flight details from web page text.
extraction_agent = Agent(
    model=local_qwen,
    output_type=list[FlightDetails],
    system_prompt="Extract all the flight details from the given text.",
)


@search_agent.tool
async def extract_flights(ctx: RunContext[Deps]) -> list[FlightDetails]:
    """Get details of all flights."""

    # Pass the usage to the search agent so requests within this agent are counted
    result = await extraction_agent.run(ctx.deps.web_page_text, usage=ctx.usage)
    logger.info("Found %d flights", len(result.output))
    return result.output


@search_agent.output_validator
async def validate_output(
    ctx: RunContext[Deps], output: FlightDetails | NoFlightFound
) -> FlightDetails | NoFlightFound:
    """Procedural validation that the flight meets the constraints."""

    if isinstance(output, NoFlightFound):
        return output

    errors: list[str] = []

    if output.origin != ctx.deps.req_origin:
        errors.append(
            f"Flight should have origin {ctx.deps.req_origin}, not {output.origin}"
        )
    if output.destination != ctx.deps.req_destination:
        errors.append(
            f"Flight should have destination {ctx.deps.req_destination}, not {output.destination}"
        )
    if output.date != ctx.deps.req_date:
        errors.append(f"Flight should be on {ctx.deps.req_date}, not {output.date}")

    if errors:
        raise ModelRetry("\n".join(errors))
    else:
        return output


class SeatPreference(BaseModel):
    row: int = Field(ge=1, le=30)
    seat: Literal["A", "B", "C", "D", "E", "F"]


class Failed(BaseModel):
    """Unable to extract a seat selection."""


# This agent is responsible for extracting the user's seat selection
seat_preference_agent = Agent(
    model=local_qwen,
    output_type=SeatPreference | Failed,
    system_prompt=(
        "Extract the user's seat preference. "
        "Seats A and F are window seats. "
        "Row 1 is the front row and has extra leg room. "
        "Rows 14, and 20 also have extra leg room."
    ),
)


# IRL this would be downloaded/extracted from a booking site,
# potentially using another agent to navigate the site...
flights_web_page = """
1. Flight SFO-AK123
- Price: $350
- Origin: San Francisco International Airport (SFO)
- Destination: Ted Stevens Anchorage International Airport (ANC)
- Date: January 10, 2025

2. Flight SFO-AK456
- Price: $370
- Origin: San Francisco International Airport (SFO)
- Destination: Fairbanks International Airport (FAI)
- Date: January 10, 2025

3. Flight SFO-AK789
- Price: $400
- Origin: San Francisco International Airport (SFO)
- Destination: Juneau International Airport (JNU)
- Date: January 20, 2025

4. Flight NYC-LA101
- Price: $250
- Origin: San Francisco International Airport (SFO)
- Destination: Ted Stevens Anchorage International Airport (ANC)
- Date: January 10, 2025

5. Flight CHI-MIA202
- Price: $200
- Origin: Chicago O'Hare International Airport (ORD)
- Destination: Miami International Airport (MIA)
- Date: January 12, 2025

6. Flight BOS-SEA303
- Price: $120
- Origin: Boston Logan International Airport (BOS)
- Destination: Ted Stevens Anchorage International Airport (ANC)
- Date: January 12, 2025

7. Flight DFW-DEN404
- Price: $150
- Origin: Dallas/Fort Worth International Airport (DFW)
- Destination: Denver International Airport (DEN)
- Date: January 10, 2025

8. Flight ATL-HOU505
- Price: $180
- Origin: Hartsfield-Jackson Atlanta International Airport (ATL)
- Destination: George Bush Intercontinental Airport (IAH)
- Date: January 10, 2025
"""


# Restrict how many requests this app can make to the LLM
usage_limits = UsageLimits(request_limit=15)


async def main():
    deps = Deps(
        web_page_text=flights_web_page,
        req_origin="SFO",
        req_destination="ANC",
        req_date=datetime.date(2025, 1, 10),
    )

    message_history: list[ModelMessage] | None = None
    usage: Usage = Usage()

    # Run the agent until a satisfactory flight is found
    while True:
        result = await search_agent.run(
            f"Find me a flight from {deps.req_origin} to {deps.req_destination} on {deps.req_date}.",
            deps=deps,
            usage=usage,
            message_history=message_history,
            usage_limits=usage_limits,
        )

        if isinstance(result.output, NoFlightFound):
            logger.info(
                f"No flight found from {deps.req_origin} to {deps.req_destination} on {deps.req_date}."
            )
            print("No flight found.")
            break

        else:
            flight = result.output

            logger.info(
                f"Flight found from {deps.req_origin} to {deps.req_destination} on {deps.req_date}.\n"
                f"Flight:\n\n"
                f"{flight}"
            )

            answer = Prompt.ask(
                "Do u want to buy this flight or keep searching? (buy/*search)",
                choices=["buy", "search", ""],
                show_choices=False,
            )

            if answer == "buy":
                seat = await find_seat(usage)
                logger.info(f"Seat found: {seat.model_dump_json(indent=4)}")

                await buy_tickets(flight, seat)
                logger.info(f"Ticket purchased")

                break

            else:
                # Inserting a message into the history, as if the user
                # asked to look for another flight
                message_history = result.all_messages(
                    output_tool_return_content="Please suggest another flight."
                )


async def find_seat(usage: Usage) -> SeatPreference:
    message_history: list[ModelMessage] | None = None

    while True:
        answer = Prompt.ask("What seat would u like?")

        result = await seat_preference_agent.run(
            answer,
            message_history=message_history,
            usage=usage,
            usage_limits=usage_limits,
        )

        if isinstance(result.output, SeatPreference):
            return result.output
        else:
            logger.info("Could no understand seat preference:\n\n" f"{answer}")
            print("Could not understand seat preference. Please try again.")
            message_history = result.all_messages()


async def buy_tickets(flight_details: FlightDetails, seat: SeatPreference):
    print(f"Purchasing flight {flight_details=!r} {seat=!r}...")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
