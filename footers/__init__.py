from fastapi import APIRouter

from .views import router as footer_router

router = APIRouter()
router.include_router(footer_router, prefix='/footers')