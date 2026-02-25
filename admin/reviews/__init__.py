from fastapi import APIRouter

from .views import router as admin_reviews_router

router = APIRouter()
router.include_router(admin_reviews_router, prefix="/reviews")