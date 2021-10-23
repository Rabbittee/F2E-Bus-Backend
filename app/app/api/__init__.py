from fastapi import APIRouter

from .routes import queries

router = APIRouter(prefix="/api")

router.include_router(queries.router)
