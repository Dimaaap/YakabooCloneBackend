from fastapi import APIRouter

from .views import router as subcategory_router

router = APIRouter()
router.include_router(subcategory_router, prefix="/subcategories")