from fastapi import APIRouter

from .views import router as user_seen_books_router

router = APIRouter()
router.include_router(user_seen_books_router, prefix="/user-seen-books")