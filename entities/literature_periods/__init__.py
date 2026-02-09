from fastapi import APIRouter

from .views import router as literature_period_router

router = APIRouter()
router.include_router(literature_period_router, prefix="/literature_period")