from fastapi import APIRouter

from .views import router as ages_router

router = APIRouter()
router.include_router(ages_router, prefix="/game-ages")