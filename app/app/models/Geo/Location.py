from pydantic import BaseModel


class GeoLocation(BaseModel):
    lon: float
    lat: float
