from fastapi import APIRouter

from .views import router as admin_promo_categories_router

router = APIRouter()
router.include_router(admin_promo_categories_router, prefix="/promo_categories")