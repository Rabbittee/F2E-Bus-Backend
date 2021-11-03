from typing import Optional
from pydantic import BaseModel
from geojson.geometry import LineString

from app.models.Constant import Direction


class GeoLocation(BaseModel):
    lon: float
    lat: float


class GeoLineString(BaseModel):
    geojson: LineString
    direction: Optional[Direction] = None
