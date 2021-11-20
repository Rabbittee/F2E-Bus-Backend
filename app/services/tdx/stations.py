from app.models.Constant import City, Lang
from app.models.Base import List
from app.models.Station import StationModel, Stop
from app.models.Geo import GeoLocation

from .network import GET


def _transform(item: dict, lang: Lang, city: City) -> StationModel:
    def _transform_stop(item: dict) -> Stop:
        return Stop(id=item['StopUID'],
                    name=item['StopName'][lang.value],
                    lang=lang)

    return StationModel(
        id=item["StationUID"],
        tdx_id=item["StationID"],
        name=item["StationName"][lang.value],
        lang=lang,
        city=city,
        address=item["StationAddress"],
        position=GeoLocation(
            lon=item["StationPosition"]["PositionLon"],
            lat=item["StationPosition"]["PositionLat"]
        ),
        route_ids=[
            stop["RouteUID"] for stop in item["Stops"]
        ],
        stops=[
            _transform_stop(stop) for stop in item["Stops"]
        ]
    )


def transform(data: List[dict], city: City) -> List[StationModel]:
    list = []

    for item in data:
        if item["StationName"].get(Lang.ZH_TW.value):
            list.append(_transform(item, Lang.ZH_TW, city))

        if item["StationName"].get(Lang.EN.value):
            list.append(_transform(item, Lang.EN, city))

    return list


async def get_stations_in(city: City) -> List[StationModel]:
    res = await GET(f"/Bus/Station/City/{city.value}")

    return transform(res.json(), city)


async def get_estimate_time_by_station(station: StationModel):
    res = await GET(
        f"/Bus/EstimatedTimeOfArrival/City/{station.city.value}/PassThrough/Station/{station.tdx_id}"
    )

    return res.json()
