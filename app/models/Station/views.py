from asyncio import gather
from typing import List

from aioredis.client import Pipeline

from app.db.cache import connection

from ..Constant import Lang
from ..Geo.Location import GeoLocation
from ..Station import StationModel, Stop
from ..Trip import Trip
from ..Route import select_by_id as route_select_by_id
from app.services.tdx import get_estimate_time_by_station


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


async def add_name_hash(name_hash):
    client = await connection()

    for name, ids in name_hash.items():
        result = await client.hsetnx(KEY.MAPPING_NAME_ID, name, ','.join(list(ids)))
        if result == 1:
            continue

        old_ids = await client.hget(KEY.MAPPING_NAME_ID, name)
        await client.hset(
            KEY.MAPPING_NAME_ID,
            name,
            ','.join(list(set(old_ids.split(',')) | ids))
        )


async def clean_name_hash():
    client = await connection()
    await client.delete(KEY.MAPPING_NAME_ID)


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

        mapping = {
            "id": station.id,
            "tdx_id": station.tdx_id,
            "name": station.name,
            "city": station.city.value
        }
        if station.address is not None:
            mapping["address"] = station.address

        (pipe.hset(
            key,
            mapping=mapping
        ).geoadd(
            KEY.STATION_GEO,
            station.position.lon,
            station.position.lat,
            station.id
        ).sadd(
            KEY.STATION_ROUTE_IDS(station.id, station.lang),
            *station.route_ids
        ).sadd(
            KEY.MAPPING_ID,
            station.id
        ).sadd(
            station.tdx_id,
            station.id
        ))

        await pipe.execute()


async def add(*stations: StationModel):
    await gather(*[add_one(station) for station in stations])


async def is_exist(**kwargs):
    client = await connection()

    for key, value in kwargs.items():
        if key == "id":
            return bool(await client.sismember(KEY.MAPPING_ID, value))

    return False


async def get_same_station_ids(id, tdx_id):
    client = await connection()
    same_stations = await client.smembers(tdx_id)
    return [
        station for station in same_stations if station != id
    ]


async def select_by_id(id: str, lang: Lang = Lang.ZH_TW):
    if not await is_exist(id=id):
        return

    client = await connection()

    # async def _select_stop_by_id(id: str):
    #     key = KEY.STOP(id, lang)
    #     dict = await client.hgetall(key)

    #     return Stop(id=dict['id'], name=dict['name'], lang=lang)

    key = KEY.STATION(id, lang)

    dict, geo, route_ids, stop_ids = await gather(
        client.hgetall(key),
        client.geopos(KEY.STATION_GEO, id),
        client.smembers(KEY.STATION_ROUTE_IDS(id, lang)),
        client.smembers(f"{key}:stops")
    )

    same_stations = await get_same_station_ids(dict['id'], dict['tdx_id'])

    if len(same_stations) > 0:
        for same_station in same_stations:
            other_key = KEY.STATION(same_station, lang)
            other_route_ids, other_stop_ids = await gather(
                client.smembers(
                    KEY.STATION_ROUTE_IDS(same_station, lang)
                ),
                client.smembers(
                    f"{other_key}:stops"
                )
            )
            stop_ids |= other_stop_ids
            route_ids |= other_route_ids

    stops = []
    # stops = await gather(
    #     *[_select_stop_by_id(id) for id in stop_ids]
    # )

    routes = await gather(
        *[route_select_by_id(id) for id in route_ids]
    )

    return StationModel(
        id=dict['id'],
        tdx_id=dict['tdx_id'],
        name=dict['name'],
        lang=lang,
        city=dict['city'],
        address=dict.get('address'),
        position=GeoLocation(lon=geo[0][0], lat=geo[0][1]),
        route_ids=route_ids,
        routes=routes,
        stops=stops,
        URL=f'/api/stations/{dict["id"]}/infomations'
    )


async def select_by_ids(ids: str, lang: Lang = Lang.ZH_TW):
    stations = []

    for id in ids:
        stations.append(await select_by_id(id, lang))

    return stations


async def get_route_ids_by_station_id(id: str, lang: Lang = Lang.ZH_TW):
    client = await connection()
    return list(
        await client.smembers(
            KEY.STATION_ROUTE_IDS(id, lang)))


async def get_routes_ids_by_station_ids(ids: List[str], lang: Lang = Lang.ZH_TW):
    routes_ids = set()

    for id in ids:
        routes_ids = routes_ids.union(
            set(await get_route_ids_by_station_id(id, lang)))

    return list(routes_ids)


async def search_by_name(name: str, lang: Lang = Lang.ZH_TW):
    client = await connection()

    id_list = []
    next = 0
    while True:
        (next, dict) = await client.hscan(KEY.MAPPING_NAME_ID, next, name, 4000)

        if bool(dict):
            for ids in dict.values():
                id_list += ids.split(',')

        if next == 0:
            break

    def _remove_same_id(stations):
        tdx_ids = set()
        filter_stations = []
        for station in stations:
            if station.tdx_id in tdx_ids:
                continue
            tdx_ids.add(station.tdx_id)
            filter_stations.append(station)

        return filter_stations

    stations = await gather(
        *[select_by_id(id, lang) for id in list(set(id_list))]
    )

    return _remove_same_id(stations)


async def search_by_position(
    position: GeoLocation,
    radius: int = 500
):
    client = await connection()
    key = KEY.STATION_GEO
    unit: str = 'm'

    station_ids = await client.georadius(
        key,
        position.lon,
        position.lat,
        radius,
        unit
    )

    return list(station_ids)


async def get_estimate_time(station_id: str):
    station = await select_by_id(station_id)

    if station is None:
        return

    stations = [station]

    def transform(item: dict):
        return Trip(
            station_id=station_id,
            route_id=item.get('RouteUID'),
            time_offset=item.get('EstimateTime', 0),
            status=item.get('StopStatus')
        )

    same_stations = await get_same_station_ids(station.id, station.tdx_id)
    if len(same_stations) > 0:
        for other_station_id in same_stations:
            other_station = await select_by_id(other_station_id)
            stations.append(other_station)

    results = []
    for station in stations:
        res = await get_estimate_time_by_station(station)
        results += list(map(transform, res))

    return results
