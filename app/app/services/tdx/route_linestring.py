from geojson import LineString
from .network import GET
from app.models.Constant import City


def get_str_within_parentheses(word: str) -> str:
    return word[
        word.find('(') + 1:
        word.rfind(')')
    ]


def transform(data: str) -> LineString:

    def _transform_str_to_tuple(token):
        return tuple(
            map(
                float,
                token.strip().split(' ')
            )
        )

    return LineString(
        list(map(
            _transform_str_to_tuple,
            get_str_within_parentheses(data).split(',')
        ))
    )


async def get_route_line_string(city: City, route_name: str) -> LineString:
    res = await GET(f"/Bus/Shape/City/{city.value}/{route_name}")

    return transform(res.json()[0].get('Geometry'))
