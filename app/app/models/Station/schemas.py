from typing import Optional, List
from pydantic import BaseModel, Field
from ..Geo import GeoLocation


class StationModel(BaseModel):
    id: str
    name: str
    address: str
    position: GeoLocation
    routeIDs: List[str]
    routes_name: Optional[List[str]] = None

    URL: Optional[str] = None
    distance: Optional[int] = None
