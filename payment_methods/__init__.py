from fastapi import APIRouter

from .views import router as payment_methods_router

router = APIRouter()
router.include_router(payment_methods_router, prefix="/payment_methods")

