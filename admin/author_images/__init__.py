from fastapi import APIRouter

from .views import router as admin_author_images_router

router = APIRouter()
router.include_router(admin_author_images_router, prefix="/author_images")