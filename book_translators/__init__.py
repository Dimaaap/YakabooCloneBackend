from fastapi import APIRouter

from .views import router as translator_router

router = APIRouter()
router.include_router(translator_router, prefix="/translators")

