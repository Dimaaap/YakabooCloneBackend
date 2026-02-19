from fastapi import APIRouter

from .views import router as admin_book_translators_router

router = APIRouter()
router.include_router(admin_book_translators_router, prefix="/book_translators")