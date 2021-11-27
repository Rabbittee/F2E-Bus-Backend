from typing import List

from app.models.Geo.Location import GeoLocation
from .schemas import StopModel


def find_nearby_stop(stops: List[StopModel], position: GeoLocation):
    min_length = float('inf')
    min_index = -1

    for i, stop in enumerate(stops):
        length = ((position.lon - stop.position.lon) ** 2 +
                  (position.lat - stop.position.lat) ** 2)**0.5

        if length < min_length:
            min_length = length
            min_index = i

    stops[min_index].nearby = True
