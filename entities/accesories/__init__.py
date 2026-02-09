from fastapi import APIRouter

from .views import router as accessories_router

router = APIRouter()
router.include_router(accessories_router, prefix="/accessories")