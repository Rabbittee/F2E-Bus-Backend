from typing import Optional, List
from pydantic import BaseModel
from app.models.Constant import Direction, BusType


class Route(BaseModel):
    id: str
    name: str
    type: BusType
    direction: Direction
    departure: str
    destination: str
    price_description: str
    authority_id: str
    operator_ids: List[str]

    URL: Optional[str] = None
    nearby_station: Optional[str] = None


class RouteList(BaseModel):
    __root__: List[Route]

    def from_json(data: str):
        return RouteList.parse_raw(data)
