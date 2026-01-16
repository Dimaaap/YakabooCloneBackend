from fastapi import APIRouter

from .views import router as reviews_reactions_router

router = APIRouter()
router.include_router(router=reviews_reactions_router, prefix="/reviews-reactions")