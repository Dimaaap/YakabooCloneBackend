from fastapi import APIRouter

from .views import router as interesting_router

router = APIRouter()
router.include_router(interesting_router, prefix="/interesting")