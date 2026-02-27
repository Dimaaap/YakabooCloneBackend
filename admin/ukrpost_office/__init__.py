from fastapi import APIRouter

from .views import router as admin_ukrpost_offices_router

router = APIRouter()
router.include_router(admin_ukrpost_offices_router, prefix="/ukrpost_offices")