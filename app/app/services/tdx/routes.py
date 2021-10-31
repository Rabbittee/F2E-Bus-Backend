from typing import List
from itertools import chain

from .network import GET
from app.models.Route import Route, SubRoute
from app.models.Constant import City, Lang


async def get_routes_in(city: City) -> List[Route]:
    res = await GET(f"/Bus/Route/City/{city.value}")

    return transform(res.json())


def _transform(item: dict, lang: Lang) -> Route:
    _lang = lang.value.split('_')[0]

    def _transform_subroute(item: dict, authority_id: str) -> SubRoute:
        _lang = "En" if lang == Lang.EN else ""

        id = authority_id + str(item['SubRouteID']) + str(item['Direction'])

        return SubRoute(
            id=id,
            name=item['SubRouteName'][lang.value],
            headsign=item.get(f'Headsign{_lang}', ''),
            direction=int(item["Direction"]),
            lang=lang,

            operator_ids=item['OperatorIDs'],

            first_bus_time=item['FirstBusTime'],
            last_bus_time=item['LastBusTime'],

            holiday_first_bus_time=item['HolidayFirstBusTime'],
            holiday_last_bus_time=item['HolidayLastBusTime']
        )

    return Route(
        id=item["RouteUID"],
        name=item["RouteName"][lang.value],
        type=int(item['BusRouteType']),
        lang=lang,

        sub_routes=[
            _transform_subroute(sub_route, item['AuthorityID']) for sub_route in item["SubRoutes"]
        ],

        authority_id=item['AuthorityID'],
        provider_id=item['ProviderID'],
        operator_ids=[
            operator['OperatorID'] for operator in item['Operators']
        ],

        departure=item[f"DepartureStopName{_lang}"],
        destination=item[f"DestinationStopName{_lang}"],
        price_description=item[f'TicketPriceDescription{_lang}'],
        fare_buffer_zone_description=item[f'FareBufferZoneDescription{_lang}']
    )


def transform(data: List[dict]) -> List[Route]:
    return list(
        chain.from_iterable(
            (
                _transform(item, Lang.ZH_TW),
                _transform(item, Lang.EN)
            ) for item in data
        )
    )
