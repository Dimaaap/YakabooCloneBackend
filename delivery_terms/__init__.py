from fastapi import APIRouter

from .views import router as delivery_terms_router

router = APIRouter()
router.include_router(delivery_terms_router, prefix="/delivery_terms")