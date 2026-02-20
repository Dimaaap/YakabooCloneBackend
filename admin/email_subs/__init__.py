from fastapi import APIRouter

from .views import router as admin_email_subs_router

router = APIRouter()
router.include_router(admin_email_subs_router, prefix="/email_subs")