from fastapi import APIRouter

from .views import router as admin_footers_router

router = APIRouter()
router.include_router(admin_footers_router, prefix="/footers")