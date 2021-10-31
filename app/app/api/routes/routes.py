from typing import List

from pydantic import BaseModel
from fastapi import APIRouter

from app.models import Route, Stop

from app.models.Stop import mock as stopMock
from app.models.Route import mock as routeMock

router = APIRouter(prefix="/routes", tags=["routes"])


@router.get("/{route_name}/infomations", response_model=Route.RouteModel)
async def route_info(route_name: str):
    route = await routeMock.search_by_name(route_name)
    return route[0]


@router.get("/{route_name}/stops", response_model=List[Stop.StopOfRoute])
async def stop_of_route(route_name: str):
    StopOfRoutes = await stopMock.search_by_name(route_name)
    return StopOfRoutes
