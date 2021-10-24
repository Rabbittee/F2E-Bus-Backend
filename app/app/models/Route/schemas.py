from typing import Optional
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
    operator_ids: list[str]

    URL: Optional[str] = None
    nearby_station: Optional[str] = None


class RouteList(BaseModel):
    __root__: list[Route]

    def from_json(data: str):
        return RouteList.parse_raw(data).__root__

    def to_json(routes: list[Route]):
        return RouteList.parse_obj(routes).json()
