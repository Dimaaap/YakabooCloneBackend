from fastapi import APIRouter

from .views import router as meest_post_offices_router

router = APIRouter()
router.include_router(meest_post_offices_router, prefix="/meest_post_offices")