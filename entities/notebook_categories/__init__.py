from fastapi import APIRouter

from .views import router as notebook_category_router

router = APIRouter()
router.include_router(notebook_category_router, prefix="/notebook_categories")