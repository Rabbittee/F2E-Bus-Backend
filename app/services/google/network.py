from enum import Enum
from urllib.parse import urlencode
import httpx
from app.config import settings

GOOGLE_MAP_API = settings.GOOGLE_MAP_API
GEOCODING_API_KEY = settings.GEOCODING_API_KEY


class TypeEnum(str, Enum):
    GEOCODE = 'geocode'


async def GET(type: TypeEnum, params: dict = {}):
    url = f"{GOOGLE_MAP_API}/{type}/json?" + \
        urlencode({"key": GEOCODING_API_KEY, **params})

    header = {
        'accept-language': 'zh-TW'
    }

    async with httpx.AsyncClient() as client:
        res = await client.get(url, headers=header)

        if res.status_code != 200:
            raise ConnectionError(
                f"GET data from google failed with {res.status_code}"
            )

        return res
