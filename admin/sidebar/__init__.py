from fastapi import APIRouter

from .views import router as admin_sidebars_router

router = APIRouter()
router.include_router(admin_sidebars_router, prefix="/sidebars")