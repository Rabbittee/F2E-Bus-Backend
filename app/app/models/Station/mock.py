from typing import List
import json
from app.models.Constant import city, lang
from app.models import Route, Station
from app.services.tdx.stations import _get_stations_in

from app.models.Route import mock as routeMock

Lang = lang.Lang.ZH_TW


class SingleTonStations:
    _instance = None
    stations: List[Station.StationModel] = []

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def get_stations(self):
        stations = await _get_stations_in(city.City.Taipei)

        stations = [
            Station.StationModel(**station) for station in json.loads(stations)
        ]

        self.stations = stations


async def search_by_name(name: str) -> Route.RouteModel:
    data = SingleTonStations()
    if not data.stations:
        await data.get_stations()

    match_stations = [
        station for station in data.stations if name in station.name
    ]

    for station in match_stations:
        station.URL = f'/api/stations/{station.name}/routes'
        station.routes_name = []

        for id in station.routeIDs:
            route = await routeMock.search_by_id(id)
            station.routes_name.append(route[0].name)

    return match_stations
