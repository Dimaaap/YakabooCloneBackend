from fastapi import APIRouter

from .views import router as search_router

router = APIRouter()
router.include_router(router=search_router, prefix="/search")