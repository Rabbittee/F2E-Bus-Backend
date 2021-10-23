from typing import Optional
from pydantic import BaseModel


class Route(BaseModel):
    name: str
    description: Optional[str] = None
    type: str = "ROUTE"
    URL: Optional[str] = None
