from fastapi import APIRouter

from .views import router as illustrator_router

router = APIRouter()
router.include_router(illustrator_router, prefix="/illustrators")