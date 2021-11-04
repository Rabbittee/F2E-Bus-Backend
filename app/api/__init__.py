from fastapi import APIRouter

from . import public, private

router = APIRouter(prefix="/api")

router.include_router(public.queries.router)
router.include_router(public.routes.router)
router.include_router(public.stations.router)

router.include_router(private.routes.router)
router.include_router(private.stations.router)
