from asyncio import gather

from aioredis.client import Pipeline
from app.db.cache import connection
from app.models.Constant import BusType, Direction, Lang

from . import RouteModel, SubRoute


class KEY:
    MAPPING_NAME_ID = "routes:name->id"
    MAPPING_ID = "routes:id"

    def ROUTE(id: str, lang: Lang):
        return f"{lang.value}:route:{id}"

    def SUB_ROUTE(id: str, lang: Lang):
        return f"{lang.value}:sub_route:{id}"


async def add_one(route: RouteModel):
    client = await connection()

    def _add_one_sub_route(pipe: Pipeline, sub_route: SubRoute):
        key = KEY.SUB_ROUTE(sub_route.id, sub_route.lang)

        (
            pipe
            .hset(key, mapping={
                'id': sub_route.id,
                'name': sub_route.name,
                'headsign': sub_route.headsign,
                'direction': sub_route.direction.value,
                'first_bus_time': sub_route.first_bus_time,
                'last_bus_time': sub_route.last_bus_time,
                'holiday_first_bus_time': sub_route.holiday_first_bus_time,
                'holiday_last_bus_time': sub_route.holiday_last_bus_time,
            })
            .sadd(f"{key}:operator_ids", *sub_route.operator_ids)
        )

    async with client.pipeline() as pipe:
        key = KEY.ROUTE(route.id, route.lang)

        for sub_route in route.sub_routes:
            _add_one_sub_route(pipe, sub_route)

            pipe.sadd(f"{key}:sub_routes", sub_route.id)

        (
            pipe
            .hset(key, mapping={
                "id": route.id,
                "name": route.name,
                "type": route.type.value,

                "authority_id": route.authority_id,
                "provider_id": route.provider_id,

                "departure": route.departure,
                "destination": route.destination,

                "price_description": route.price_description,
                "fare_buffer_zone_description": route.fare_buffer_zone_description,
            })
            .sadd(f"{key}:operator_ids", *route.operator_ids)
            .sadd(KEY.MAPPING_ID, route.id)
            .hset(KEY.MAPPING_NAME_ID, route.name, route.id)
        )

        await pipe.execute()


async def add(*routes: RouteModel):
    await gather(*[add_one(route) for route in routes])


async def is_exist(**kwargs):
    client = await connection()

    for key, value in kwargs.items():
        if key == "id":
            return await client.sismember(f"routes:id", value)

        if key == "name":
            return await client.hexists(f"routes:name->id", value)

    return False


async def select_by_id(id: str, lang: Lang = Lang.ZH_TW):
    if not await is_exist(id=id):
        return

    key = KEY.ROUTE(id, lang)

    client = await connection()

    async def _select_sub_route_by_id(pipe: Pipeline, id: str) -> SubRoute:
        key = KEY.SUB_ROUTE(id, lang)

        dict, operator_ids = await (
            pipe
            .hgetall(key)
            .smembers(f"{key}:operator_ids")
            .execute()
        )

        return SubRoute(
            id=dict['id'],
            name=dict['name'],
            headsign=dict['headsign'],
            direction=Direction(int(dict['direction'])),
            lang=lang,
            operator_ids=operator_ids,
            first_bus_time=dict['first_bus_time'],
            last_bus_time=dict['last_bus_time'],
            holiday_first_bus_time=dict['holiday_first_bus_time'],
            holiday_last_bus_time=dict['holiday_last_bus_time'],
        )

    async with client.pipeline() as pipe:
        dict, operator_ids, sub_routes_ids = await (
            pipe
            .hgetall(key)
            .smembers(f"{key}:operator_ids")
            .smembers(f"{key}:sub_routes")
            .execute()
        )

        sub_routes = []

        for id in sub_routes_ids:
            sub_routes.append(
                await _select_sub_route_by_id(pipe, id)
            )

        return RouteModel(
            id=dict['id'],
            name=dict['name'],
            type=BusType(int(dict['type'])),
            lang=lang,

            sub_routes=sub_routes,

            authority_id=dict['authority_id'],
            provider_id=dict['provider_id'],
            operator_ids=operator_ids,

            departure=dict['departure'],
            destination=dict['destination'],
            price_description=dict['price_description'],
            fare_buffer_zone_description=dict['fare_buffer_zone_description']
        )


async def select_by_name(name: str, lang: Lang = Lang.ZH_TW):
    client = await connection()

    if not await is_exist(name=name):
        return

    id = await client.hget(f"routes:name->id", name)

    return await select_by_id(id, lang)


async def search_by_name(name: str, lang: Lang = Lang.ZH_TW):
    '''
    Supported glob-style patterns:
        - h?llo matches hello, hallo and hxllo
        - h*llo matches hllo and heeeello
        - h[ae]llo matches hello and hallo, but not hillo
        - h[^e]llo matches hallo, hbllo, ... but not hello
        - h[a-b]llo matches hallo and hbllo
    '''

    client = await connection()

    tasks = []

    next = 0
    while True:
        (next, dict) = await client.hscan(KEY.MAPPING_NAME_ID, next, name)

        tasks += [select_by_id(id, lang) for id in dict.values()]

        if next == 0:
            break

    return await gather(*tasks)
