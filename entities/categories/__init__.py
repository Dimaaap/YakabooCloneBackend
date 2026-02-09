from fastapi import APIRouter

from .views import router as banner_router

router = APIRouter()
router.include_router(banner_router, prefix="/categories")