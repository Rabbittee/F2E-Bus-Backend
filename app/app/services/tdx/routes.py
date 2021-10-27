from .network import GET
from app.models.Route import Route, RouteList
from app.models.Constant import City, Lang

from app.db import cacheByStr


def _keygen(city: City, lang: Lang = Lang.ZH_TW):
    return f"routes:{city.value}:{lang.value}"


async def _get_routes_in(city: City, lang: Lang = Lang.ZH_TW):
    res = await GET(f"/Bus/Route/City/{city.value}")

    if res.status_code != 200:
        raise ConnectionError(
            f"Fetch routes from TDX failed with {res.status_code}")

    return RouteList(
        __root__=_transform(res.json(), lang)
    ).json()


def _transform(data: dict, lang: Lang) -> list[Route]:
    routes: list[Route] = []

    lang = str(lang.value)
    _lang = lang.split('_')[0]

    for item in data:
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

    return routes


async def get_routes_in(city: City, lang: Lang = Lang.ZH_TW):
    return RouteList.from_json(
        await cacheByStr(
            _keygen,
            _get_routes_in
        )(city, lang)
    )
