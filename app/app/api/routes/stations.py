from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter(prefix="/stations", tags=["stations"])


@router.get("/{station_name}/routes", response_model=List)
async def query(route_name: str):

    return []