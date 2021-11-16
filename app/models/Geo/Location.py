from typing import List, Optional
from pydantic import BaseModel
from geojson.geometry import LineString
from statistics import mean

from ..Constant import Direction


class GeoLocation(BaseModel):
    lon: float
    lat: float


class GeoLineString(BaseModel):
    geojson: LineString
    direction: Optional[Direction] = None


class Geocode(BaseModel):
    location: GeoLocation
    address: str


class Bbox(BaseModel):
    left: float
    bottom: float
    right: float
    top: float


def str_to_location(location: str) -> GeoLocation:
    lat, lon = location.split(',')
    return GeoLocation(lon=float(lon), lat=float(lat))


def find_bounding(locations: List[GeoLocation]) -> Bbox:

    bbox = Bbox(
        left=float("inf"),
        bottom=float("inf"),
        right=float("-inf"),
        top=float("-inf")
    )

    for location in locations:
        if location.lat < bbox.bottom:
            bbox.bottom = location.lat

        if location.lat > bbox.top:
            bbox.top = location.lat

        if location.lon < bbox.left:
            bbox.left = location.lon

        if location.lon > bbox.right:
            bbox.right = location.lon

    return bbox


def get_centroid(points: List[GeoLocation]) -> GeoLocation:
    return GeoLocation(
        lat=mean([p.lat for p in points]),
        lon=mean([p.lon for p in points])
    )
