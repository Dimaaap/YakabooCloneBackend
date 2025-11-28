from fastapi import APIRouter

from .views import router as new_post_postomats_router

router = APIRouter()
router.include_router(new_post_postomats_router, prefix="/new_post_postomats")