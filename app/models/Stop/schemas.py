from typing import List, Optional
from pydantic import BaseModel

from ..Geo import GeoLocation
from ..Constant import DirectionInfo


class StopModel(BaseModel):
    id: str
    name: str
    position: GeoLocation
    estimate_time: Optional[int] = None


class StopOfRoute(BaseModel):
    route_name: str
    direction: DirectionInfo
    stops: List[StopModel]
