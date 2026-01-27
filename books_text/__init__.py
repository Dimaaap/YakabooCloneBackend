from fastapi import APIRouter

from .views import router as books_text_router

router = APIRouter()
router.include_router(books_text_router, prefix="/book_text")