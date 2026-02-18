from fastapi import APIRouter

from .views import router as admin_authors_router

router = APIRouter()
router.include_router(admin_authors_router, prefix="/authors")