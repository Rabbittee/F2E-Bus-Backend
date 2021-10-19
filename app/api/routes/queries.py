
from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    tags=["query"]
)


@router.get("/")
async def query(item_id: str):
    ...
