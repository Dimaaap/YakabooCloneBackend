from fastapi import APIRouter

from .views import router as admin_cities_router

router = APIRouter()
router.include_router(admin_cities_router, prefix="/cities")