from fastapi import APIRouter

from .views import router as knowledge_router

router = APIRouter()
router.include_router(knowledge_router, prefix="/knowledge")
