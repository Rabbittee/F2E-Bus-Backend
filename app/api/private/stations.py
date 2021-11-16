from fastapi import APIRouter

from app.models import Station
from app.models.Constant import City
from app.services.tdx import get_stations_in

router = APIRouter(prefix="/private/stations", tags=["private.stations"])


@router.get("/{city}")
async def add_stations(city: City):
    stations = await get_stations_in(city)

    try:
        name_hash = {}
        for station in stations:
            await Station.add_one(station)
            if station.name not in name_hash:
                name_hash[station.name] = set()

            name_hash[station.name].add(station.id)

        await Station.add_name_hash(name_hash)

    except Exception as error:
        print(error)

        return {
            "message": "Failed to add stations",
            "exception_message": error
        }

    return {
        "message": "write stations from TDX into Redis successful",
        "num_of_stations": len(stations),
    }
