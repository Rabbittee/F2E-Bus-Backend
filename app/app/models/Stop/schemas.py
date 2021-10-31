from pydantic import BaseModel
from ..Geo import GeoLocation


class StopModel(BaseModel):
    id: str
    name: str
    position: GeoLocation
