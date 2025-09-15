from fastapi import APIRouter

from .view import router as gifts_router

router = APIRouter()
router.include_router(gifts_router, prefix="/gifts")