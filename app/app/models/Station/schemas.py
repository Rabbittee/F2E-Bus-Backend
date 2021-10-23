from typing import Optional
from pydantic import BaseModel, Field


class Station(BaseModel):
    name: str
    type: str = Field("STATION", const=True)
    URL: Optional[str] = None
    distance: int
