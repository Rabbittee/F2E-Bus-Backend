from asyncio import gather

from aioredis.client import Pipeline
from app.db.cache import connection
from app.models.Constant import Lang
from app.models.Geo.Location import GeoLocation
from app.models.Station import StationModel, Stop


class KEY:
    STATION_GEO = "stations:positions"

    MAPPING_ID = "stations:id"

    def STATION(id: str, lang: Lang):
        return f"{lang.value}:station:{id}"

    def STOP(id: str, lang: Lang):
        return f"{lang.value}:stop:{id}"


async def add_one(station: StationModel):
    client = await connection()

    def _add_stop(pipe: Pipeline, stop: Stop):
        key = KEY.STOP(stop.id, stop.lang)

        pipe.hset(key, mapping={
            "id": stop.id,
            "name": stop.name,
        })

    async with client.pipeline() as pipe:
        key = KEY.STATION(station.id, station.lang)

        for stop in station.stops:
            _add_stop(pipe, stop)

            pipe.sadd(f"{key}:stops", stop.id)

        (
            pipe
            .hset(key, mapping={
                "id": station.id,
                "name": station.name,
                "address": station.address,
            })
            .geoadd(
                KEY.STATION_GEO,
                station.position.lon,
                station.position.lat,
                station.id
            )
            .sadd(f"{key}:route_ids", *station.route_ids)
            .sadd(KEY.MAPPING_ID, station.id)
        )

        await pipe.execute()


async def add(*stations: StationModel):
    await gather(*[add_one(station) for station in stations])


async def is_exist(**kwargs):
    pass


async def select_by_id(id: str, lang: Lang = Lang.ZH_TW):
    client = await connection()

    async def _select_stop_by_id(pipe: Pipeline, id: str):
        key = KEY.STOP(id, lang)
        dict, = await pipe.hgetall(key).execute()

        return Stop(
            id=dict['id'],
            name=dict['name'],
            lang=lang
        )

    async with client.pipeline() as pipe:
        key = KEY.STATION(id, lang)

        dict, geo, route_ids, stop_ids = await (
            pipe
            .hgetall(key)
            .geopos(KEY.STATION_GEO, id)
            .smembers(f"{key}:route_ids")
            .smembers(f"{key}:stops")
            .execute()
        )

        stops = []
        for id in stop_ids:
            stops.append(
                await _select_stop_by_id(pipe, id)
            )

        return StationModel(
            id=dict['id'],
            name=dict['name'],
            lang=lang,
            address=dict['address'],
            position=GeoLocation(
                lon=geo[0][0],
                lat=geo[0][1]
            ),
            route_ids=route_ids,
            stops=stops
        )


async def search_by_name(name: str, lang: Lang = Lang.ZH_TW):
    pass
