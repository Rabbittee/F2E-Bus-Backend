from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter

from app.services.tdx import get_stop_of_route
from app.models import Route, Stop
from app.models.Constant import Direction
from app.models.Constant.city import City

router = APIRouter(prefix="/routes", tags=["routes"])


class StopOfRoute(BaseModel):
    departure: Optional[str] = None
    destination: Optional[str] = None
    direction: Direction
    stops: List[Stop.StopModel]


@router.get("/{route_name}/stops", response_model=List[StopOfRoute])
async def query(route_name: str):

    routeInfo = await Route.search_by_name(route_name)
    routeInfoMap = {}
    for route in routeInfo:
        routeInfoMap[route.direction] = {
            'departure': route.departure,
            'destination': route.destination
        }
    print()

    routeStops = await get_stop_of_route(City.Taipei, route_name)
    for route in routeStops:
        if route.direction not in routeInfoMap:
            continue
        route.departure = routeInfoMap[route.direction]['departure']
        route.destination = routeInfoMap[route.direction]['destination']

    return routeStops
