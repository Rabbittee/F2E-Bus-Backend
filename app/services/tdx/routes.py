from typing import List
from itertools import chain

from app.models.Stop.schemas import StopModel
from app.models.Route.schemas import RouteModel, SubRoute
from app.models.Constant import City, Lang

from .network import GET


async def get_routes_in(city: City) -> List[RouteModel]:
    res = await GET(f"/Bus/Route/City/{city.value}")

    return transform(res.json())


def _transform(item: dict, lang: Lang) -> RouteModel:
    _lang = lang.value.split('_')[0]

    def _transform_subroute(item: dict, authority_id: str) -> SubRoute:
        _lang = "En" if lang == Lang.EN else ""

        id = authority_id + str(item['SubRouteID']) + str(item['Direction'])

        return SubRoute(
            id=id,
            name=item['SubRouteName'].get(lang.value, ""),
            headsign=item.get(f'Headsign{_lang}', ''),
            direction=int(item["Direction"]),
            lang=lang,
            operator_ids=item['OperatorIDs'],
            first_bus_time=item.get('FirstBusTime', ''),
            last_bus_time=item.get('LastBusTime', ''),
            holiday_first_bus_time=item.get('HolidayFirstBusTime', ''),
            holiday_last_bus_time=item.get('HolidayLastBusTime', '')
        )

    return RouteModel(
        id=item["RouteUID"],
        name=item["RouteName"][lang.value],
        type=int(item['BusRouteType']),
        lang=lang,
        city=City(item['City']),
        sub_routes=[
            _transform_subroute(sub_route, item['AuthorityID'])
            for sub_route in item["SubRoutes"]
        ],
        authority_id=item['AuthorityID'],
        provider_id=item['ProviderID'],
        operator_ids=[
            operator['OperatorID'] for operator in item['Operators']
        ],
        departure=item.get(f"DepartureStopName{_lang}", ""),
        destination=item.get(f"DestinationStopName{_lang}", ""),
        price_description=item.get(f'TicketPriceDescription{_lang}', ''),
        fare_buffer_zone_description=item.get(
            f'FareBufferZoneDescription{_lang}', '')
    )


def transform(data: List[dict]) -> List[RouteModel]:
    return list(
        chain.from_iterable(
            (_transform(item, Lang.ZH_TW), _transform(item, Lang.EN))
            for item in data
        )
    )


async def get_stop_of_route(
    city: City,
    route_name: str,
    direction: int
) -> List[StopModel]:
    res = await GET(
        f"/Bus/StopOfRoute/City/{city.value}/{route_name}",
        {
            "$filter": f"Direction eq {direction}"
        }
    )

    return res.json()


async def get_route_estimated_time(
    city: City,
    route_name: str,
    direction: int
):
    res = await GET(
        f"/Bus/EstimatedTimeOfArrival/City/{city.value}/{route_name}",
        {
            "$top": 1000,
            "$filter": f"Direction eq {direction}"
        }
    )

    return res.json()


async def get_route_schedule(route: RouteModel):
    res = await GET(f'/Bus/Schedule/City/{route.city.value}/{route.name}')

    return list(filter(
        lambda item: item['RouteUID'] == route.id,
        res.json()
    ))[0]
