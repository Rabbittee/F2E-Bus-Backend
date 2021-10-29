from typing import List, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.models import Route, Station

router = APIRouter(prefix="/queries", tags=["query"])


class MatchItem(BaseModel):
    routes: List[Route.Route]
    stations: List[Station.Station]


@router.get("/recommend", response_model=MatchItem)
async def query(
    q: str = None,
    location: Optional[str] = Query(None,
                                    regex="^\d{2}.?\d{0,7},\d{3}.?\d{0,7}$"),
):

    match_items = {"routes": [], "stations": []}
    if q is None and location is None:
        return match_items

    if q is not None:
        match_items["routes"] = await Route.search_by_name(q)
        match_items["stations"] = Station.find(q)

    # if geo location
    # > 站牌:距離排序
    # > 路線:顯示最近站牌，下班車

    return match_items
