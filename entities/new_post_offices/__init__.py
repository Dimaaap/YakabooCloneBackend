from fastapi import APIRouter

from .views import router as new_post_offices_router

router = APIRouter()
router.include_router(new_post_offices_router, prefix="/new_post_offices")