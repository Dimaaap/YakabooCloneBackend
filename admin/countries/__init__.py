from fastapi import APIRouter

from .views import router as admin_countries_router

router = APIRouter()
router.include_router(admin_countries_router, prefix="/countries")