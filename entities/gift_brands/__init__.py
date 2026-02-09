from fastapi import APIRouter

from .views import router as gift_brand_router

router = APIRouter()
router.include_router(gift_brand_router, prefix="/gift_brands")