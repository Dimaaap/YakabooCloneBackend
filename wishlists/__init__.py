from fastapi import APIRouter

from .views import router as wishlist_router

router = APIRouter()
router.include_router(router=wishlist_router, prefix="/wishlist")