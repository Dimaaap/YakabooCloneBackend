from fastapi import APIRouter

from .views import router as admin_books_router

router = APIRouter()
router.include_router(admin_books_router, prefix="/books")