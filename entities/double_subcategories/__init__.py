from fastapi import APIRouter

from .views import router as double_subcategory_router

router = APIRouter()
router.include_router(double_subcategory_router, prefix="/double_subcategories")