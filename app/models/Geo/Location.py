from typing import Optional
from pydantic import BaseModel
from geojson.geometry import LineString

from ..Constant import Direction


class GeoLocation(BaseModel):
    lon: float
    lat: float


class GeoLineString(BaseModel):
    geojson: LineString
    direction: Optional[Direction] = None


def str_to_location(location: str):
    lat, lon = location.split(',')
    return GeoLocation(lon=float(lon), lat=float(lat))
