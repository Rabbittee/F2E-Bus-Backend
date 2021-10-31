from fastapi import APIRouter

from .routes import queries, routes, stations

router = APIRouter(prefix="/api")

router.include_router(queries.router)
router.include_router(routes.router)
router.include_router(stations.router)
