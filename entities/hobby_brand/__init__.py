from fastapi import APIRouter

from .views import router as hobby_brand_router

router = APIRouter()
router.include_router(hobby_brand_router, prefix="/hobby-brands")