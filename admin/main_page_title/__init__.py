from fastapi import APIRouter

from .views import router as admin_main_page_titles_router

router = APIRouter()
router.include_router(admin_main_page_titles_router, prefix="/main_page_title")