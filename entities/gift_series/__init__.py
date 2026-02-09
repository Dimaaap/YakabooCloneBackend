from fastapi import APIRouter

from .views import router as gift_series_router

router = APIRouter()
router.include_router(gift_series_router, prefix="/gift-series")
