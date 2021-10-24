import httpx
import time
import asyncio

from wsgiref.handlers import format_date_time
from hmac import digest
from hashlib import sha1
from base64 import b64encode

from app.models.Route import Route, RouteList
from app.models.Constant import City, Lang
from app.config import settings
from app.db import cache

HOST = settings.TDX_HOST
API_ID = settings.TDX_API_ID
API_KEY = settings.TDX_API_KEY


def signature(date: str, key: str):
    return b64encode(
        digest(
            key=bytes(key, "utf-8"),
            msg=bytes(f'x-date: {date}', "utf-8"),
            digest=sha1
        )
    ).decode()


def hmac(username: str, signature: str):
    return "hmac " + ",".join(
        list(
            map(
                lambda x: f'{x[0]}="{x[1]}"',
                {
                    'username': username,
                    'algorithm': 'hmac-sha1',
                    'headers': 'x-date',
                    'signature': signature
                }.items()
            )
        )
    )


async def GET(url: str):
    current_time = format_date_time(time.time())

    headers = {
        'Authorization': hmac(
            username=API_ID,
            signature=signature(current_time, API_KEY)
        ),
        'x-date': current_time,
    }

    async with httpx.AsyncClient() as client:
        return await client.get(HOST + url, headers=headers)


async def get_routes_in(city: City, lang: Lang = Lang.ZH_TW):
    cache_key = f"routes:{city.value}:{lang.value}"

    if await cache.client.exists(cache_key):
        data = await cache.client.get(cache_key)

        return RouteList.from_json(data)

    res = await GET(f"/Bus/Route/City/{city.value}")

    if not res.ok:
        raise ConnectionError(
            f"Fetch routes from TDX failed with {res.status_code}")

    routes: list[Route] = []

    lang = str(lang.value)
    _lang = lang.split('_')[0]

    for item in res.json():
        id = item["RouteUID"]
        name = item["RouteName"][lang]
        departure = item[f"DepartureStopName{_lang}"]
        destination = item[f"DestinationStopName{_lang}"]
        price_description = item[f'TicketPriceDescription{_lang}']
        bus_type = item['BusRouteType']
        authority = item['AuthorityID']
        operator_ids = list(
            map(
                lambda operator: operator['OperatorID'],
                item['Operators']
            )
        )

        for route in item["SubRoutes"]:
            direction = route["Direction"]

            routes.append(
                Route(**{
                    'id': id,
                    'name': name,
                    'type': bus_type,
                    'direction': direction,
                    'departure': departure if direction else destination,
                    'destination': destination if direction else departure,
                    'price_description': price_description,
                    'authority_id': authority,
                    'operator_ids': operator_ids
                })
            )

    cache.client.set(cache_key, RouteList.to_json(routes))

    return routes


async def main():
    print(await get_routes_in(City.Taipei))

asyncio.run(main())
