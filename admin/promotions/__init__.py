from fastapi import APIRouter

from .views import router as admin_promotions_router

router = APIRouter()
router.include_router(admin_promotions_router, prefix="/promotions")