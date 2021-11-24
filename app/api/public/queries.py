from typing import List, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.models import Station, Route
from app.models.Geo.Location import Bbox, GeoLocation, find_bounding, get_centroid, str_to_location
from app.models.Base import Error
from app.services.google.geocoding import get_geocode

router = APIRouter(prefix="/queries", tags=["query"])


class MatchItem(BaseModel):
    routes: List[Route.schemas.RouteModel]
    stations: List[Station.schemas.StationModel]
    bbox: Optional[Bbox] = None
    center: Optional[GeoLocation] = None


@router.get("/recommend", response_model=MatchItem)
async def query(
    q: str = None,
    location: Optional[str] = Query(
        None,
        regex="^\d{2}.?\d{0,7},\d{3}.?\d{0,7}$"
    ),
    radius:  Optional[int] = Query(200, ge=0, le=3000),
    use_geocode_api: bool = False,
    with_bounding_center: bool = False,
):

    async def _filter_location(q, position, radius, match_items):
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
            match_items["stations"] = filter_by_id(
                match_items["stations"],
                near_by_station_ids
            )

            match_items["routes"] = filter_by_id(
                match_items["routes"],
                near_by_route_ids
            )
        return match_items

    match_items = {"routes": [], "stations": []}
    if q is None and location is None:
        raise Error.CustomException(Error.ErrorType.RESOURCE_NOT_FOUND)

    if q is not None:
        match_items["routes"] = await Route.search_by_name(f'*{q}*')
        match_items["stations"] = await Station.search_by_name(f'*{q}*')

    if location:
        position = str_to_location(location)

        match_items = await _filter_location(
            q, position, radius, match_items
        )

    if use_geocode_api and len(match_items["stations"]) + len(match_items["routes"]) == 0:
        geocodes = await get_geocode(q)
        match_items = await _filter_location(
            None, geocodes[0].location, radius, match_items
        )

    match_items["stations"] = remove_none_from(match_items["stations"])
    match_items["routes"] = remove_none_from(match_items["routes"])

    if len(match_items["stations"]) + len(match_items["routes"]) == 0:
        raise Error.CustomException(Error.ErrorType.RESOURCE_NOT_FOUND)

    if with_bounding_center and len(match_items["stations"]) > 0:
        locations = [station.position for station in match_items["stations"]]
        match_items["bbox"] = find_bounding(locations)
        match_items["center"] = get_centroid(locations)

    return match_items


@router.get("/geocoding", response_model=List)
async def geocoding(keyword: str):
    positions = await get_geocode(keyword)

    return positions


def filter_by_id(source, ids):
    return [
        s for s in source if s.id in ids
    ]


def remove_none_from(ls):
    return list(filter(None, ls))
