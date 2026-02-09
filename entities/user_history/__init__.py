from fastapi import APIRouter

from .views import router as user_search_story_router

router = APIRouter()
router.include_router(user_search_story_router, prefix="/user-search-story")