from typing import List

from .network import GET, TypeEnum
from app.models.Geo import GeoLocation, Geocode


def _transform(data):
    if data['status'] != 'OK':
        return []

    locations = []
    for result in data['results']:
        location = result['geometry']['location']
        address = result['formatted_address']
        locations.append(
            Geocode(
                location=GeoLocation(lat=location['lat'], lon=location['lng']),
                address=address
            )
        )
    return locations


async def get_geocode(address: str) -> List[Geocode]:

    res = await GET(TypeEnum.GEOCODE, {
        "address": address,
        "region": "tw"
    })

    return _transform(res.json())
