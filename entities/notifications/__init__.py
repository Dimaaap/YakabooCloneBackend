from fastapi import APIRouter

from .views import router as notifications_router

router = APIRouter()
router.include_router(notifications_router, prefix="/notifications")