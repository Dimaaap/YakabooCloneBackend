from fastapi import APIRouter

from .views import router as admin_orders_router

router = APIRouter()
router.include_router(admin_orders_router, prefix="/orders")