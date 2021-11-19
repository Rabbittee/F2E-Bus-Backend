from fastapi import APIRouter
from typing import List

from app.models.Base import Error
from app.models import Station
from app.models.Trip import Trip

router = APIRouter(prefix="/stations", tags=["stations"])


@router.get("/{station_id}/informations", response_model=Station.StationModel)
async def query(station_id: str):
    station = await Station.select_by_id(station_id)

    if station is None:
        raise Error.CustomException(Error.ErrorType.RESOURCE_NOT_FOUND)

    return station


@router.get("/{station_id}/estimatetime", response_model=List[Trip])
async def estimate_time(station_id: str):
    res = await Station.get_estimate_time(station_id)

    if res is None:
        raise Error.CustomException(Error.ErrorType.RESOURCE_NOT_FOUND)

    return res
