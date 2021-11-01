from app.services.tdx import get_stations_in
from app.models.Station.views import add, select_by_id
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

    async def test_select_by_id_with_exist_id(self):
        r = await select_by_id("TPE10")

        self.assertIsNotNone(r)
