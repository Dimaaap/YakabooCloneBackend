from fastapi import APIRouter

from .views import router as contacts_router

router = APIRouter()
router.include_router(contacts_router, prefix="/contacts")