from fastapi import APIRouter

from .views import router as admin_promo_codes_router

router = APIRouter()
router.include_router(admin_promo_codes_router, prefix="/promo_codes")