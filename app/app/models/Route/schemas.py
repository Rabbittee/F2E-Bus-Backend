from typing import Dict, Optional, List
from pydantic import BaseModel
from app.models.Constant import Direction, BusType, Lang, DirectionInfo


class SubRoute(BaseModel):
    id: str
    name: str
    headsign: str
    direction: Direction
    lang: Lang

    operator_ids: List[str]

    first_bus_time: str
    last_bus_time: str

    holiday_first_bus_time: str
    holiday_last_bus_time: str


class RouteModel(BaseModel):
    id: str
    name: str
    type: BusType
    lang: Lang

    sub_routes: List[SubRoute]

    departure: str
    destination: str

    authority_id: str
    provider_id: str
    operator_ids: List[str]

    price_description: str  # 票價
    fare_buffer_zone_description: str  # 收費緩衝區

    directions: Optional[Dict[Direction, DirectionInfo]] = None
    URL: Optional[str] = None
    nearby_station: Optional[str] = None
