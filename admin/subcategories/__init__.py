from fastapi import APIRouter

from .views import router as admin_subcategories_router

router = APIRouter()
router.include_router(admin_subcategories_router, prefix="/subcategories")