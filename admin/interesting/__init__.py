from fastapi import APIRouter

from .views import router as admin_interesting_router

router = APIRouter()
router.include_router(admin_interesting_router, prefix="/interesting")