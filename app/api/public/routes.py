from typing import List

from fastapi import APIRouter

from app.models.Geo.Location import GeoLineString
from app.models import Route, Stop
from app.services.tdx.route_linestring import get_route_line_string

router = APIRouter(prefix="/routes", tags=["routes"])


@router.get("/{route_id}/infomations", response_model=Route.RouteModel)
async def route_info(route_id: str):
    route = await Route.select_by_id(route_id)
    return route


@router.get("/{route_id}/stops", response_model=List[Stop.StopOfRoute])
async def stop_of_route(route_id: str):
    StopOfRoutes = await Route.select_stop_of_route(route_id)

    return StopOfRoutes


@router.get("/{route_id}/line_string", response_model=List[GeoLineString])
async def line_string(route_id: str):
    route = await Route.select_by_id(route_id)

    return await get_route_line_string(route.city, route.name)
