from fastapi import APIRouter

from .views import router as admin_review_reactions_router

router = APIRouter()
router.include_router(admin_review_reactions_router, prefix="/review_reactions")