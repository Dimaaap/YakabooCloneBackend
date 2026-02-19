from fastapi import APIRouter

from .views import router as admin_contacts_router

router = APIRouter()
router.include_router(admin_contacts_router, prefix="/contacts")