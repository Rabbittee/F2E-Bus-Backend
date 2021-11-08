from typing import List, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.models import Station, Route
from app.models.Geo.Location import str_to_location
from app.models.Base import Error

router = APIRouter(prefix="/queries", tags=["query"])


class MatchItem(BaseModel):
    routes: List[Route.schemas.RouteModel]
    stations: List[Station.schemas.StationModel]


@router.get("/recommend", response_model=MatchItem)
async def query(
    q: str = None,
    location: Optional[str] = Query(
        None,
        regex="^\d{2}.?\d{0,7},\d{3}.?\d{0,7}$"
    ),
    radius:  Optional[int] = Query(500, ge=0, le=3000)
):

    def _filter_by_id(source, ids):
        return [
            s for s in source if s.id in ids
        ]

    match_items = {"routes": [], "stations": []}
    if q is None and location is None:
        raise Error.CustomException(Error.ErrorType.RESOURCE_NOT_FOUND)

    if q is not None:
        match_items["routes"] = await Route.search_by_name(f'*{q}*')
        match_items["stations"] = await Station.search_by_name(f'*{q}*')

    if location:
        position = str_to_location(location)
        near_by_station_ids = await Station.search_by_position(
            position,
            radius
        )
        near_by_route_ids = await Station.get_routes_ids_by_station_ids(
            near_by_station_ids
        )

        if q is None:
            match_items["stations"] = await Station.select_by_ids(
                near_by_station_ids
            )
            match_items["routes"] = await Route.select_by_ids(
                near_by_route_ids
            )
        else:
            match_items["stations"] = _filter_by_id(
                match_items["stations"],
                near_by_station_ids
            )

            match_items["routes"] = _filter_by_id(
                match_items["routes"],
                near_by_route_ids
            )

    return match_items
