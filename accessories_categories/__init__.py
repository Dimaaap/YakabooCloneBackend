from fastapi import APIRouter

from .views import router as accessory_category_router

router = APIRouter()
router.include_router(accessory_category_router, prefix="/accessories-categories")
