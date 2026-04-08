from fastapi import APIRouter

from .views import router as publishing_banners_router

router = APIRouter()
router.include_router(publishing_banners_router, prefix="/publishing_banners")