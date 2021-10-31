from enum import Enum
from pydantic import BaseModel


class Direction(Enum):
    Departure = 0
    Destination = 1
    Loop = 2
    Unknown = 255


class DirectionInfo(BaseModel):
    departure: str
    destination: str
    direction: Direction
