from fastapi import APIRouter

from .views import router as book_series_router

router = APIRouter()
router.include_router(book_series_router, prefix="/book_series")
