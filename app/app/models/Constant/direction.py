from enum import Enum


class Direction(Enum):
    Departure = 0
    Destination = 1
    Loop = 2
    Unknown = 255
