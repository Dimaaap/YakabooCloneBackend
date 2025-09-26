from fastapi import APIRouter

from .views import router as hobby_router

router = APIRouter()
router.include_router(hobby_router, prefix="/hobbies")