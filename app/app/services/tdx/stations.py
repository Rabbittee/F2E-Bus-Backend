from .network import GET
from models.Constant import City, Lang
from models.Base import List
from models.Station import StationModel, Stop
from models.Geo import GeoLocation


def _transform(item: dict, lang: Lang) -> StationModel:
    def _transform_stop(item: dict) -> Stop:
        return Stop(id=item['StopUID'],
                    name=item['StopName'][lang.value],
                    lang=lang)

    return StationModel(
        id=item["StationUID"],
        name=item["StationName"][lang.value],
        lang=lang,
        address=item["StationAddress"],
        position=GeoLocation(lon=item["StationPosition"]["PositionLon"],
                             lat=item["StationPosition"]["PositionLat"]),
        route_ids=[stop["RouteUID"] for stop in item["Stops"]],
        stops=[_transform_stop(stop) for stop in item["Stops"]])


def transform(data: List[dict]) -> List[StationModel]:
    list = []

    for item in data:
        if item["StationName"].get(Lang.ZH_TW.value):
            list.append(_transform(item, Lang.ZH_TW))

        if item["StationName"].get(Lang.EN.value):
            list.append(_transform(item, Lang.EN))

    return list


async def get_stations_in(city: City) -> List[StationModel]:
    res = await GET(f"/Bus/Station/City/{city.value}")

    return transform(res.json())
