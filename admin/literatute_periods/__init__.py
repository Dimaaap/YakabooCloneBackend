from fastapi import APIRouter

from .views import router as admin_literature_periods_router

router = APIRouter()
router.include_router(admin_literature_periods_router, prefix="/literature_periods")