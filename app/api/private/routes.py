
from fastapi import APIRouter

from app.models.Constant import City
from app.models import Route
from app.services.tdx import get_routes_in

router = APIRouter(prefix="/private/routes", tags=["private.routes"])


@router.get("/{city}")
async def add_routes(city: City):
    routes = await get_routes_in(city)

    try:
        await Route.add(*routes)
    except Exception as error:
        print(error)

        return {
            "message": "Failed to add routes",
            "exception_message": error
        }

    return {
        "message": "write routes from TDX into Redis successful",
        "num_of_routes": len(routes),
        "num_of_sub_routes": sum([len(route.sub_routes) for route in routes])
    }
