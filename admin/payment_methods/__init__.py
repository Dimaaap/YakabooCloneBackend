from fastapi import APIRouter

from .views import router as admin_payment_methods_router

router = APIRouter()
router.include_router(admin_payment_methods_router, prefix="/payment_methods")