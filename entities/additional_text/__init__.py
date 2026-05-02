from fastapi import APIRouter

from .views import router as additional_text_router

router = APIRouter()
router.include_router(additional_text_router, prefix="/additional_text")
