from fastapi import APIRouter

from .views import router as hobby_subcategory_router

router = APIRouter()
router.include_router(hobby_subcategory_router, prefix="/hobby-subcategories")