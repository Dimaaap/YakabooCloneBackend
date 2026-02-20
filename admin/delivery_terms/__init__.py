from fastapi import APIRouter

from .views import router as admin_delivery_terms_router

router = APIRouter()
router.include_router(admin_delivery_terms_router, prefix="/delivery_terms")