from typing import Optional
from pydantic import BaseModel, Field


class Route(BaseModel):
    name: str
    type: str = Field("ROUTE", const=True)
    URL: Optional[str] = None
    nearby_station: Optional[str] = None
