from fastapi import APIRouter

from .views import router as publishing_router

router = APIRouter()
router.include_router(publishing_router, prefix="/publishing")