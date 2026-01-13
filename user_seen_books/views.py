from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, UserSeenBook
from . import crud
from .schema import UserSeenBooksSchema

router = APIRouter(tags=["User`s Seen Books"])


@router.post("/add")
async def add_seen_book(user_email: str, book_id: int,
                        session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    return await crud.add_book_to_seen(session, user_email, book_id)


@router.get("/all/{user_email}")
async def get_all_user_seen_books(
        user_email: str,
        session: AsyncSession=Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_all_user_seen_books(session, user_email)