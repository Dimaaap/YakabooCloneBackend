from fastapi import APIRouter

from .views import router as ukrpost_offices_router

router = APIRouter()
router.include_router(ukrpost_offices_router, prefix="/ukrpost_offices")