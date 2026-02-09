from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import schema
from . import crud

router = APIRouter(tags=["User`s search history"])


@router.post("/add")
async def add_term_to_search_history(user_email: str, term: schema.UserHistoryCreate,
                                     session: AsyncSession = Depends(db_helper.scoped_session_dependency)):


    return await crud.add_term_to_search_history(session, user_email, term.term, term.is_active)


@router.get("/all/{user_email}")
async def get_all_user_search_story(
        user_email: str,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_all_user_search_terms(session, user_email)


@router.patch("/update/{user_email}")
async def clear_search_history(
        user_email: str,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.clear_all_user_search_terms(session, user_email)


