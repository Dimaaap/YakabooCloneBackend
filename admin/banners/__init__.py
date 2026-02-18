from fastapi import APIRouter

from .views import router as admin_banners_router

router = APIRouter()
router.include_router(admin_banners_router, prefix="/banners")