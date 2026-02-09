from fastapi import APIRouter

from .views import router as promo_code_usage_router

router = APIRouter()
router.include_router(promo_code_usage_router, prefix="/promo-codes-usage")

