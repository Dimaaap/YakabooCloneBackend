from fastapi import APIRouter

from .views import router as gift_subcategory_router

router = APIRouter()
router.include_router(gift_subcategory_router, prefix="/gift-subcategories")