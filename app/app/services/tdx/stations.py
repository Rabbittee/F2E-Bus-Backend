from .network import GET
from app.models.Constant import City, Lang
from app.models.Base import List
from app.models.Station import Station
from app.models.Geo import GeoLocation
from app.db.cache import cacheByStr


def _keygen(city: City, lang: Lang = Lang.ZH_TW):
    return f"stations:{city.value}:{lang.value}"


async def _get_stations_in(city: City, lang: Lang = Lang.ZH_TW):
    res = await GET(f"/Bus/Station/City/{city.value}")

    return List(__root__=[
        Station(**{
            "id": item["StationUID"],
            "name": item["StationName"][lang.value],
            "address": item["StationAddress"],
            "position": GeoLocation(**{
                "hash": item["StationPosition"]["GeoHash"],
                "lon": item["StationPosition"]["PositionLon"],
                "lat": item["StationPosition"]["PositionLat"]
            }),
            "routeIDs": list(
                map(
                    lambda item: item["RouteUID"],
                    item["Stops"]
                )
            )
        })
        for item in res.json()
    ]).json()


async def get_stations_in(city: City, lang: Lang = Lang.ZH_TW):
    return List.from_json(
        await cacheByStr(
            _keygen,
            _get_stations_in
        )(city, lang)
    )
