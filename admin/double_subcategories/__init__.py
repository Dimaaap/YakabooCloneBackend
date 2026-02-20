from fastapi import APIRouter

from .views import router as admin_double_subcategories_router

router = APIRouter()
router.include_router(admin_double_subcategories_router, prefix="/double_subcategories")