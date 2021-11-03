from typing import List, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.models import Station, Route

# from app.services.tdx import get_stations_in
# from app.models.Station.views import add
# from app.models.Constant import City
# from app.services.tdx import get_routes_in
# from app.models.Route.views import add

router = APIRouter(prefix="/queries", tags=["query"])

# async def test_add_with():
#   stations = await get_stations_in(City.Taipei)
#   print("stations: ", len(stations))
#   await add(*stations)
#   routes = await get_routes_in(City.Taipei)
#   print("routes: ", len(routes))
#   print("sub_routes: ", sum([len(route.sub_routes) for route in routes]))
#   await add(*routes)


class MatchItem(BaseModel):
    routes: List[Route.schemas.RouteModel]
    stations: List[Station.schemas.StationModel]


@router.get("/recommend", response_model=MatchItem)
async def query(
    q: str = None,
    location: Optional[str] = Query(None,
                                    regex="^\d{2}.?\d{0,7},\d{3}.?\d{0,7}$"),
):

    # await test_add_with()

    match_items = {"routes": [], "stations": []}
    if q is None and location is None:
        return match_items

    if q is not None:
        match_items["routes"] = await Route.search_by_name(f'*{q}*')
        match_items["stations"] = await Station.search_by_name(f'*{q}*')

    # ToDo
    # if geo location
    # > 站牌:距離排序
    # > 路線:顯示最近站牌，下班車
    return match_items
