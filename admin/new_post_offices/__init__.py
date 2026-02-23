from fastapi import APIRouter

from .views import router as admin_new_post_offices_router

router = APIRouter()
router.include_router(admin_new_post_offices_router, prefix="/new_post_offices")