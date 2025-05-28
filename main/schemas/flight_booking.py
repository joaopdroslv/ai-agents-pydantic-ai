import datetime
from typing import Literal

from pydantic import BaseModel, Field


class FlightDetails(BaseModel):
    flight_number: str
    price: int
    origin: str = Field(description="Three-letter airport code.")
    destination: str = Field(description="Three-letter airport code.")
    date: datetime.date


class NoFlightFound(BaseModel):
    """When no valid flights is found."""


class SeatPreference(BaseModel):
    row: int = Field(ge=1, le=30)
    seat: Literal["A", "B", "C", "D", "E", "F"]


class Failed(BaseModel):
    """Unable to extract a seat selection."""
