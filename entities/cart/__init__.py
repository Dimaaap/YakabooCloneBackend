from fastapi import APIRouter

from .views import router as cart_router

router = APIRouter()
router.include_router(cart_router, prefix="/cart")