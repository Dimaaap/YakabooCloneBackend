from fastapi import APIRouter

from .views import router as cart_item_router

router = APIRouter()
router.include_router(router=cart_item_router, prefix="/cart-item")