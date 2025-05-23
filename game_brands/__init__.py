from fastapi import APIRouter

from .views import router as brands_router

router = APIRouter()
router.include_router(brands_router, prefix="/game-brands")