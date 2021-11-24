from typing import Optional, List
from pydantic import BaseModel


from ..Geo import GeoLocation
from ..Constant import Lang, City


class Stop(BaseModel):
    id: str
    name: str
    lang: Lang


class StationModel(BaseModel):
    id: str
    tdx_id: str

    name: str
    lang: Lang

    address: Optional[str] = None
    position: GeoLocation
    city: City

    stops: List[Stop]

    route_ids: List[str]
    routes: Optional[List] = None

    URL: Optional[str] = None
    distance: Optional[int] = None
