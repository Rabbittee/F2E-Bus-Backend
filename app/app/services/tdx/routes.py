from typing import Optional
from pydantic import BaseModel

from .network import GET
from app.models.Route import RouteModel
from app.models.Constant import City, Lang, Direction
from app.models.Base import List
from app.models import Stop


async def get_routes_in(city: City, lang: Lang = Lang.ZH_TW):
    res = await GET(f"/Bus/Route/City/{city.value}")

    return _transform(res.json(), lang)


async def get_stop_of_route(city: City, route: str, lang: Lang = Lang.ZH_TW):
    res = await GET(f"/Bus/StopOfRoute/City/{city.value}/{route}")
    data = res.json()

    class StopOfRoute(BaseModel):
        departure: Optional[str] = None
        destination: Optional[str] = None
        direction: Direction
        stops: List[Stop.StopModel]

    stopOfRoutes: List[StopOfRoute] = []

    for route in data:
        stops = [{
            'name': stop['StopName']['Zh_tw'],
            'id': stop['StopUID'],
            'position': {
                'hash': stop['StopPosition']['GeoHash'],
                'lon': stop['StopPosition']['PositionLon'],
                'lat': stop['StopPosition']['PositionLat']
            }
        } for stop in route['Stops']]

        stopOfRoutes.append(
            StopOfRoute(**{
                "direction": route['Direction'],
                'stops': stops
            }))

    return stopOfRoutes


def _transform(data: dict, lang: Lang) -> List[RouteModel]:
    routes: List[RouteModel] = []

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
            map(lambda operator: operator['OperatorID'], item['Operators']))

        for route in item["SubRoutes"]:
            direction = route["Direction"]

            routes.append(
                RouteModel(
                    **{
                        'id': id,
                        'name': name,
                        'type': bus_type,
                        'direction': direction,
                        'departure': departure if direction else destination,
                        'destination': destination if direction else departure,
                        'price_description': price_description,
                        'authority_id': authority,
                        'operator_ids': operator_ids
                    }))

    return routes
