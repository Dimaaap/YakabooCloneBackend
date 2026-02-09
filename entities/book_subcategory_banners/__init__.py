from fastapi import APIRouter

from .views import router as book_subcategory_banners_router

router = APIRouter()
router.include_router(book_subcategory_banners_router, prefix="/book_subcategory_banners")