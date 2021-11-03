from asyncio import gather

from aioredis.client import Pipeline
from db.cache import connection
from models.Constant import Lang
from models.Geo.Location import GeoLocation
from models.Station import StationModel, Stop
from models.Route import select_by_id as route_select_by_id


class KEY:
    STATION_GEO = "stations:positions"

    MAPPING_ID = "stations:id"
    MAPPING_NAME_ID = "stations:name->id"

    def STATION(id: str, lang: Lang):
        return f"{lang.value}:station:{id}"

    def STATION_ROUTE_IDS(id: str, lang: Lang):
        return f"{KEY.STATION(id, lang)}:route_ids"

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

        (pipe.hset(key,
                   mapping={
                       "id": station.id,
                       "name": station.name,
                       "address": station.address,
                   }).geoadd(KEY.STATION_GEO, station.position.lon,
                             station.position.lat, station.id).sadd(
                                 KEY.STATION_ROUTE_IDS(station.id,
                                                       station.lang),
                                 *station.route_ids).sadd(
                                     KEY.MAPPING_ID,
                                     station.id).hset(KEY.MAPPING_NAME_ID,
                                                      station.name,
                                                      station.id))

        await pipe.execute()


async def add(*stations: StationModel):
    await gather(*[add_one(station) for station in stations])


async def is_exist(**kwargs):
    client = await connection()

    for key, value in kwargs.items():
        if key == "id":
            return bool(await client.sismember(KEY.MAPPING_ID, value))

    return False


async def select_by_id(id: str, lang: Lang = Lang.ZH_TW):
    if not await is_exist(id=id):
        return

    client = await connection()

    async def _select_stop_by_id(pipe: Pipeline, id: str):
        key = KEY.STOP(id, lang)
        dict, = await pipe.hgetall(key).execute()

        return Stop(id=dict['id'], name=dict['name'], lang=lang)

    async with client.pipeline() as pipe:
        key = KEY.STATION(id, lang)

        dict, geo, route_ids, stop_ids = await (pipe.hgetall(key).geopos(
            KEY.STATION_GEO, id).smembers(KEY.STATION_ROUTE_IDS(
                id, lang)).smembers(f"{key}:stops").execute())

        stops = []
        for id in stop_ids:
            stops.append(await _select_stop_by_id(pipe, id))

        routes = []
        for id in route_ids:
            routes.append(await route_select_by_id(id))

        return StationModel(id=dict['id'],
                            name=dict['name'],
                            lang=lang,
                            address=dict['address'],
                            position=GeoLocation(lon=geo[0][0], lat=geo[0][1]),
                            route_ids=route_ids,
                            routes=routes,
                            stops=stops,
                            URL=f'/api/stations/{dict["id"]}/infomations')


async def search_by_name(name: str, lang: Lang = Lang.ZH_TW):
    client = await connection()

    tasks = []

    next = 0
    while True:
        (next, dict) = await client.hscan(KEY.MAPPING_NAME_ID, next, name)

        if bool(dict):
            tasks += [select_by_id(id, lang) for id in dict.values()]

        if next == 0:
            break

    return await gather(*tasks)
