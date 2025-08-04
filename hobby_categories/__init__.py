from fastapi import APIRouter

from .views import router as hobby_category_router

router = APIRouter()
router.include_router(hobby_category_router, prefix="/hobby-categories")