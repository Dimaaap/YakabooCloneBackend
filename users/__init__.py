from fastapi import APIRouter

from .views import router as user_router

router = APIRouter()
router.include_router(router=user_router, prefix="/auth")