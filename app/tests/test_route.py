from app.models.Constant.city import City
from app.models.Route.views import add, select_by_id, select_by_name, search_by_name
from app.services.tdx import get_routes_in

from unittest import IsolatedAsyncioTestCase

# async def test_add():
#     routes = await get_routes_in(City.Taipei)

#     await add(*routes)


class TestRoute(IsolatedAsyncioTestCase):

    async def test_select_by_id_with_exist_id(self):
        r = await select_by_id("TPE11764")

        self.assertIsNotNone(r)

    async def test_select_by_id_with_not_exist_id(self):
        r = await select_by_id("APPLE")

        self.assertIsNone(r)

    async def test_select_by_name_with_exist_name(self):
        r = await select_by_name("234")

        self.assertIsNotNone(r)

    async def test_select_by_name_with_not_exist_name(self):
        r = await select_by_name("APPLE")

        self.assertIsNone(r)

    async def test_search_by_name_with_explicit_term(self):
        r = await search_by_name("234")

        self.assertIsNotNone(r)

    async def test_search_by_name_with_glob(self):
        r = await search_by_name("23*")

        self.assertIsNotNone(r)
