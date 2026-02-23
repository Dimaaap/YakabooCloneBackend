from fastapi import APIRouter

from .views import router as admin_meest_post_offices_router

router = APIRouter()
router.include_router(admin_meest_post_offices_router, prefix="/meest_post_offices")