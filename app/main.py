from asyncio import run
from asyncio.tasks import gather
from app.models.Constant.city import City
from app.models.Route.views import add, select_by_id, select_by_name, search_by_name
from app.services.tdx import get_routes_in


async def test_add():
    routes = await get_routes_in(City.Taipei)

    print(
        "routes: ",
        len(routes)
    )

    print(
        "sub_routes: ",
        sum([len(route.sub_routes) for route in routes])
    )

    # await add(*routes)


async def test_select_by_id():
    r = await select_by_id("TPE11764")

    print(r)


async def test_select_by_name():
    r = await select_by_name("234")

    print(r)


async def test_search_by_name():
    r = await search_by_name("2*")

    print(r)


async def main():
    await gather(
        # test_add(),
        test_select_by_id(),
        # test_select_by_name(),
        # test_search_by_name()
    )

run(main())
