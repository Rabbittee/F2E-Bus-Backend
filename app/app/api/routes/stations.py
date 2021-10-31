from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter

from app.models.Station import mock as stationMock

router = APIRouter(prefix="/stations", tags=["stations"])


@router.get("/{station_name}/infomations", response_model=List)
async def query(route_name: str):
    stations = await stationMock.search_by_name(route_name)

    return stations[0]