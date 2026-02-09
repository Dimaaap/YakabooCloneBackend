from fastapi import APIRouter

from .views import router as gift_category_router

router = APIRouter()
router.include_router(gift_category_router, prefix="/gift-categories")