from fastapi import APIRouter

from app.models import Station

router = APIRouter(prefix="/stations", tags=["stations"])


@router.get("/{station_id}/infomations", response_model=Station.StationModel)
async def query(station_id: str):
    station = await Station.select_by_id(station_id)

    return station
