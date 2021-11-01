from app.services.tdx import get_stations_in
from app.models.Station.views import add, select_by_id, is_exist, search_by_name
from app.models.Constant import City

from unittest import IsolatedAsyncioTestCase


class TestStation(IsolatedAsyncioTestCase):

    async def test_add_with(self):
        stations = await get_stations_in(City.Taipei)

        print(
            "stations: ",
            len(stations)
        )

        await add(*stations)

    async def test_is_exist_with_exist_id(self):
        r = await is_exist(id="TPE10")

        self.assertIsNotNone(r)

    async def test_select_by_id_with_exist_id(self):
        r = await select_by_id("TPE10")

        self.assertIsNotNone(r)

    async def test_search_by_name_with_exist_name(self):
        r = await search_by_name("八勢里")

        self.assertTrue(r)

    async def test_search_by_name_with_glob(self):
        r = await search_by_name("八勢*")

        self.assertTrue(r)

    async def test_search_by_name_with_empty_str(self):
        r = await search_by_name("")

        self.assertFalse(r)
