from typing import List

from .network import GET, TypeEnum
from app.models.Geo import GeoLocation


def _transform(data):
    if data['status'] != 'OK':
        return []

    locations = []
    for result in data['results']:
        location = result['geometry']['location']
        locations.append(
            GeoLocation(lat=location['lat'], lon=location['lng'])
        )
    return locations


async def get_geolocation(address: str) -> List[GeoLocation]:

    res = await GET(TypeEnum.GEOCODE, f"address={address}")

    return _transform(res.json())
