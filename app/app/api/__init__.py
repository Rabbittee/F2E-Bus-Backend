from fastapi import APIRouter

from .routes import queries, routes

router = APIRouter(prefix="/api")

router.include_router(queries.router)
router.include_router(routes.router)
