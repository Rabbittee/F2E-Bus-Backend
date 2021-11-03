from typing import Optional, List
from pydantic import BaseModel

from ..Geo import GeoLocation
from app.models.Constant import Lang
# from app.models.Route import RouteModel


class Stop(BaseModel):
    id: str
    name: str
    lang: Lang


class StationModel(BaseModel):
    id: str
    name: str
    lang: Lang

    address: str
    position: GeoLocation

    stops: List[Stop]

    route_ids: List[str]
    # routes_name: Optional[List[str]] = None
    routes: Optional[List] = None

    URL: Optional[str] = None
    distance: Optional[int] = None
