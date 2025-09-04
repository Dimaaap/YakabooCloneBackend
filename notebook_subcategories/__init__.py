from fastapi import APIRouter

from .view import router as notebook_subcategory_router

router = APIRouter()
router.include_router(notebook_subcategory_router, prefix="/subcategory")