from typing import List

from . import schemas

items = [{
    "name": "市政府(市府)",
    "type": "STATION",
    "URL": "/stations/市政府%28市府%29",
    "distance": 130
}]


def find(q: str) -> List[schemas.Station]:
    return [item for item in items if q in item['name']]