from fastapi import APIRouter

from .views import router as sidebar_router

router = APIRouter()
router.include_router(sidebar_router, prefix="/authors")