from typing import Optional
from pydantic import BaseModel, Field
from ..Geo import GeoLocation


class Station(BaseModel):
    id: str
    name: str
    address: str
    position: GeoLocation
    routeIDs: list[str]

    type: str = Field("STATION", const=True)
    URL: Optional[str] = None
    distance: int
