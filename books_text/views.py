from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud

router = APIRouter(tags=["books_text"])


@router.get("/")
async def get_books_text(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    books_text = await crud.get_book_text(session)
    return books_text


@router.post("/create")
async def create_books_text(
        new_text: str,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_text = await crud.create_book_text(session, new_text)
    return {"text": new_text}