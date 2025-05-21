from fastapi import APIRouter

from .views import router as game_series_router

router = APIRouter()
router.include_router(game_series_router, prefix="/game-series")
