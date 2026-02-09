from fastapi import APIRouter

from .views import router as accessory_brand_router

router = APIRouter()
router.include_router(accessory_brand_router, prefix="/accessories-brands")