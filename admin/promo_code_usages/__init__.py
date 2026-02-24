from fastapi import APIRouter

from .views import router as admin_promo_code_usages_router

router = APIRouter()
router.include_router(admin_promo_code_usages_router, prefix="/promo_code_usages")