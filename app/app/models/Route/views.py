from asyncio import gather
from app.db.cache import connection
from app.models.Constant import BusType, Direction

from . import Route


class KEY:
    MAPPING_NAME_ID = f"routes:name->id"


async def add_one(route: Route):
    client = await connection()

    async with client.pipeline() as pipe:
        key = f"route:{route.id}"

        await (
            pipe
            .hset(key, mapping={
                "id": route.id,
                "name": route.name,
                "type": route.type.value,
                "direction": route.direction.value,
                "departure": route.departure,
                "destination": route.destination,
                "price_description": route.price_description,
                "authority_id": route.authority_id,
            })
            .sadd(f"{key}:operator_ids", *route.operator_ids)
            .sadd(f"routes:id", route.id)
            .hset(f"routes:name->id", route.name, route.id)
            .execute()
        )


async def add(*routes: Route):
    await gather(*[
        add_one(route) for route in routes
    ])


async def is_exist(**kwargs):
    client = await connection()

    for key, value in kwargs.items():
        if key == "id":
            return await client.sismember(f"routes:id", value)

        if key == "name":
            return await client.hexists(f"routes:name->id", value)

    return False


async def select_by_id(id: str):
    if not await is_exist(id=id):
        return

    key = f"route:{id}"

    client = await connection()

    async with client.pipeline() as pipe:
        dict, operator_ids = await (
            pipe
            .hgetall(key)
            .smembers(f"{key}:operator_ids")
            .execute()
        )

        return Route(**{
            "id": dict['id'],
            "name": dict['name'],
            "type": BusType(int(dict['type'])),
            "direction": Direction(int(dict['direction'])),
            "departure": dict['departure'],
            "destination": dict['destination'],
            "price_description": dict['price_description'],
            "authority_id": dict['authority_id'],
            "operator_ids": operator_ids
        })


async def select_by_name(name: str):
    client = await connection()

    if not await is_exist(name=name):
        return

    id = await client.hget(f"routes:name->id", name)

    return await select_by_id(id)


async def search_by_name(name: str):
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

        tasks += [select_by_id(id) for id in dict.values()]

        if next == 0:
            break

    return await gather(*tasks)
