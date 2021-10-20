from typing import Optional

from fastapi import APIRouter, Query

router = APIRouter(prefix="/queries", tags=["query"])


@router.get("/recommend")
async def query(q: str,
                location: Optional[str] = Query(
                    None,
                    min_length=6,
                    max_length=22,
                    regex="^\d{2}.?\d{0,7},\d{3}.?\d{0,7}$")):

    return {"location": location, "q": q}
