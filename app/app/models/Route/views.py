from typing import List

from . import schemas

items = [
    {
        "name": "266 承德幹線",
        "type": "ROUTE",
        "URL": "/buses/266%20承德幹線/stations"
    },
    {
        "name": "26",
        "type": "ROUTE",
        "URL": "/buses/26/stations"
    },
]


def find(q: str) -> List[schemas.Route]:
    return [item for item in items if q in item['name']]