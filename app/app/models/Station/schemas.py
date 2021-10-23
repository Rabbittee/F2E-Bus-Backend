from typing import Optional
from pydantic import BaseModel


class Station(BaseModel):
    name: str
    description: Optional[str] = None
    type: str = "STATION"
    URL: Optional[str] = None
