from typing import Optional, List
from pydantic import BaseModel
from app.models.Constant import Direction, BusType


class RouteModel(BaseModel):
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
