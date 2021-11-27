from typing import List
from geojson import LineString

from app.models.Constant import City
from app.models.Geo.Location import GeoLineString

from .network import GET


def get_str_within_parentheses(word: str) -> str:
    return word[word.find('(') + 1:word.rfind(')')]


def transform(data: str) -> LineString:
    def _transform_str_to_tuple(token):
        return tuple(map(float, token.strip().split(' ')))

    return LineString(
        list(
            map(_transform_str_to_tuple,
                get_str_within_parentheses(data).split(','))))


async def get_route_line_string(
    city: City,
    route_name:  str,
    direction: int
) -> List[GeoLineString]:
    baseUrl = f"/Bus/Shape/City/{city.value}/{route_name}"

    res = await GET(
        baseUrl,
        {
            "$filter": f"Direction eq {direction}"
        }
    )

    if len(res.json()) == 0:
        res = await GET(baseUrl)

    return [
        GeoLineString(
            geojson=transform(row.get('Geometry')),
            direction=row.get('Direction')
        ) for row in res.json()
    ]
