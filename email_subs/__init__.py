from fastapi import APIRouter

from .views import router as subs_router

router = APIRouter()
router.include_router(router=subs_router, prefix="/subs")