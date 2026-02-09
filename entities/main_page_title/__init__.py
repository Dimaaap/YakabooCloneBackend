from fastapi import APIRouter

from .views import router as page_title_router

router = APIRouter()
router.include_router(page_title_router, prefix="/page-title")