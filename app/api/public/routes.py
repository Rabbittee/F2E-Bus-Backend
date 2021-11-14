from typing import List

from fastapi import APIRouter

from app.models.Geo.Location import GeoLineString
from app.models import Route, Stop
from app.models.Base import Error
from app.services.tdx.route_linestring import get_route_line_string

router = APIRouter(prefix="/routes", tags=["routes"])


@router.get("/{route_id}/infomations", response_model=Route.RouteModel)
async def route_info(route_id: str):
    route = await Route.select_by_id(route_id)

    if route is None:
        raise Error.CustomException(Error.ErrorType.RESOURCE_NOT_FOUND)

    return route


@router.get("/{route_id}/stops", response_model=Stop.StopOfRoute)
async def stop_of_route(
    route_id: str,
    direction: int,
    estimate_time: bool = False
):
    routes = await Route.select_stop_of_route(route_id, direction, estimate_time)

    if routes is None:
        raise Error.CustomException(Error.ErrorType.RESOURCE_NOT_FOUND)

    return routes[0]


@router.get("/{route_id}/line_string", response_model=List[GeoLineString])
async def line_string(route_id: str, direction: int):
    route = await Route.select_by_id(route_id)

    if route is None:
        raise Error.CustomException(Error.ErrorType.RESOURCE_NOT_FOUND)

    return await get_route_line_string(route.city, route.name, direction)
