from typing import List, Optional
from app.models.Constant.direction import DirectionInfo
from pydantic import BaseModel

from ..Geo import GeoLocation
from ..Constant import DirectionInfo


class StopModel(BaseModel):
    id: str
    name: str
    position: GeoLocation


class StopOfRoute(BaseModel):
    route_name: str
    direction: DirectionInfo
    stops: List[StopModel]
