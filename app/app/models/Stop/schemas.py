from typing import List
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
