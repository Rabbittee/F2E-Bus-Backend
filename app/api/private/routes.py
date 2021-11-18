
from fastapi import APIRouter

from app.models.Constant import City
from app.models import Route
from app.services.tdx import get_routes_in

router = APIRouter(prefix="/private/routes", tags=["private.routes"])


@router.get("/{city}")
async def add_routes(city: City):
    routes = await get_routes_in(city)

    try:
        name_hash = {}
        for route in routes:
            await Route.add_one(route)
            if route.name not in name_hash:
                name_hash[route.name] = set()

            name_hash[route.name].add(route.id)

        await Route.add_name_hash(name_hash)

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


@router.delete('/clean_name_hash')
async def clean_name_hash():
    try:
        await Route.clean_name_hash()

    except Exception as error:
        print(error)

        return {
            "message": "Failed to clean routes name hash",
            "exception_message": error
        }

    return {
        "message": "clean routes name from Redis successful",
    }
