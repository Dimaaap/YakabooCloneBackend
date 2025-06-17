from fastapi import APIRouter

from .views import router as cities_router

router = APIRouter()
router.include_router(cities_router, prefix="/cities")