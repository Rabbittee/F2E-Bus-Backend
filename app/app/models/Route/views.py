from typing import List

from app.services import tdx
from app.models.Constant import City
from . import schemas


async def find(q: str) -> List[schemas.Route]:

    routes = await tdx.get_routes_in(City.Taipei)
    return [route for route in routes if q in route['name']]