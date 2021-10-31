from typing import List
from app.models.Constant import city, lang
from app.models import Route
from app.models.Constant.direction import DirectionInfo
from app.services.tdx import get_routes_in

Lang = lang.Lang.ZH_TW


class SingleTonRoutes:
    _instance = None
    routes: List[Route.RouteModel] = []

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def get_routes(self):
        routes = await get_routes_in(city.City.Taipei)

        def merge(routes):
            idMap = {}
            for route in routes:
                direction = DirectionInfo(departure=route.departure,
                                          destination=route.destination,
                                          direction=route.direction)
                if route.id not in idMap:
                    idMap[route.id] = route
                    idMap[route.id].directions = {}

                idMap[route.id].directions[route.direction] = direction

            return list(idMap.values())

        self.routes = merge(routes)


async def search_by_name(name: str) -> Route.RouteModel:
    data = SingleTonRoutes()
    if not data.routes:
        await data.get_routes()
    match_routes = [route for route in data.routes if name in route.name]
    for route in match_routes:
        route.URL = f'/api/routes/{route.name}/stops'

    return match_routes


async def search_by_id(id: str) -> Route.RouteModel:
    data = SingleTonRoutes()
    if not data.routes:
        await data.get_routes()

    return [route for route in data.routes if id == route.id]
