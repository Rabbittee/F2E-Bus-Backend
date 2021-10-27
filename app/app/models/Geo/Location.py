from pydantic import BaseModel


class GeoLocation(BaseModel):
    hash: str
    lon: float
    lat: float
