from fastapi import APIRouter

from .views import router as admin_publishing_router

router = APIRouter()
router.include_router(admin_publishing_router, prefix="/publishing")