from fastapi import APIRouter

from .views import router as promo_code_router

router = APIRouter()
router.include_router(promo_code_router, prefix="/promo-codes")

