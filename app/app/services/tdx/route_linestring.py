from typing import List
from geojson import LineString
from .network import GET
from models.Constant import City
from models.Geo.Location import GeoLineString


def get_str_within_parentheses(word: str) -> str:
    return word[word.find('(') + 1:word.rfind(')')]


def transform(data: str) -> LineString:
    def _transform_str_to_tuple(token):
        return tuple(map(float, token.strip().split(' ')))

    return LineString(
        list(
            map(_transform_str_to_tuple,
                get_str_within_parentheses(data).split(','))))


async def get_route_line_string(city: City,
                                route_name: str) -> List[GeoLineString]:
    res = await GET(f"/Bus/Shape/City/{city.value}/{route_name}")

    return [
        GeoLineString(geojson=transform(row.get('Geometry')),
                      direction=row.get('Direction')) for row in res.json()
    ]
