from asyncio import run
from asyncio.tasks import gather
from app.models.Constant.city import City
from app.models.Station.views import add, select_by_id
from app.services.tdx import get_stations_in


async def test_add():
    stations = await get_stations_in(City.Taipei)

    await add(*stations)


async def test_select_by_id():
    print(
        await select_by_id("TPE10")
    )


async def main():
    await gather(
        # test_add(),
        test_select_by_id(),
        # test_select_by_name(),
        # test_search_by_name()
    )

run(main())
