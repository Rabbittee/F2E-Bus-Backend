from os import register_at_fork
from typing import List

from app.services.tdx.routes import get_stop_of_route
from app.models.Constant import city, lang
from app.models import Route
from app.models.Route import mock

from .schemas import StopOfRoute

Lang = lang.Lang.ZH_TW


async def search_by_name(name: str) -> Route.RouteModel:

    routesInfo = await mock.search_by_name(name)

    StopOfRoutes = []
    for route in routesInfo:
        routeStops = await get_stop_of_route(city.City.Taipei, route.name)
        for routeStop in routeStops:
            StopOfRoutes.append(
                StopOfRoute(
                    **{
                        **routeStop.dict(),
                        **{
                            'route_name': route.name,
                            'direction': route.directions[routeStop.direction]
                        }
                    }))

    return StopOfRoutes
