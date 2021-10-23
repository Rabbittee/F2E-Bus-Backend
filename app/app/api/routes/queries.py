from typing import List, Union, Optional

from fastapi import APIRouter, Query

from app.models import Route

router = APIRouter(prefix="/queries", tags=["query"])


@router.get("/recommend", response_model=List[Union[Route.schemas.Route]])
async def query(
    q: str = None,
    location: Optional[str] = Query(None,
                                    regex="^\d{2}.?\d{0,7},\d{3}.?\d{0,7}$"),
):

    match_items = []
    if q is None and location is None:
        return match_items

    if q is not None:
        match_items += Route.views.find(q)

    return match_items
