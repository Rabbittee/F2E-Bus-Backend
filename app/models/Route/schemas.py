from enum import Enum
from typing import Optional, List
from pydantic import BaseModel
from ..Constant import BusType, Lang, Direction, Day, City


class SubRoute(BaseModel):
    id: str
    name: str
    headsign: str
    direction: Direction
    lang: Lang

    operator_ids: List[str]

    first_bus_time: Optional[str] = None
    last_bus_time: Optional[str] = None

    holiday_first_bus_time: Optional[str] = None
    holiday_last_bus_time: Optional[str] = None


class RouteModel(BaseModel):
    id: str
    name: str
    type: BusType
    lang: Lang
    city: City

    sub_routes: List[SubRoute]

    departure: str
    destination: str

    authority_id: str
    provider_id: str
    operator_ids: List[str]

    price_description: Optional[str] = None  # 票價
    fare_buffer_zone_description: Optional[str] = None  # 收費緩衝區

    URL: Optional[str] = None
    nearby_station: Optional[str] = None


class TimetableType(str, Enum):
    Flexible = 'flexible'
    Regular = 'regular'


class Timetable(BaseModel):
    day: Day
    type: TimetableType


class FlexibleTimetable(Timetable):
    type = TimetableType.Flexible
    max_headway: int
    min_headway: int
    start_time: str
    end_time: str


class RegularTimetable(Timetable):
    type = TimetableType.Regular
    arrival_time: str
