from fastapi import APIRouter

from .views import router as author_facts_router

router = APIRouter()
router.include_router(author_facts_router, prefix="/author_facts")
