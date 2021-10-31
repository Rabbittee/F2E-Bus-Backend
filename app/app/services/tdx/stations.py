from itertools import chain
from .network import GET
from app.models.Constant import City, Lang
from app.models.Base import List
from app.models.Station import StationModel, Stop
from app.models.Geo import GeoLocation


def _transform(item: dict, lang: Lang) -> StationModel:

    def _transform_stop(item: dict) -> Stop:
        return Stop(
            id=item['StopUID'],
            name=item['StopName'][lang.value],
            lang=lang
        )

    return StationModel(
        id=item["StationUID"],
        name=item["StationName"].get(lang.value, ""),
        lang=lang,

        address=item["StationAddress"],

        position=GeoLocation(
            hash=item["StationPosition"]["GeoHash"],
            lon=item["StationPosition"]["PositionLon"],
            lat=item["StationPosition"]["PositionLat"]
        ),

        routeIDs=[
            stop["RouteUID"] for stop in item["Stops"]
        ],

        stops=[
            _transform_stop(stop) for stop in item["Stops"]
        ]
    )


def transform(data: List[dict]) -> List[StationModel]:
    return list(
        chain.from_iterable(
            (
                _transform(item, Lang.ZH_TW),
                _transform(item, Lang.EN)
            ) for item in data
        )
    )


async def get_stations_in(city: City) -> List[StationModel]:
    res = await GET(f"/Bus/Station/City/{city.value}")

    return transform(res.json())
