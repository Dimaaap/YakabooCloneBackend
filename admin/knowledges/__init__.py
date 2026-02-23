from fastapi import APIRouter

from .views import router as admin_knowledge_router

router = APIRouter()
router.include_router(admin_knowledge_router, prefix="/knowledge")