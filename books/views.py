from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import BookSchema, BookCreate
from core.models import db_helper
from . import crud

router = APIRouter(tags=["books"])

@router.get('/all', response_model=list[BookSchema])
async def get_all_books(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    books = await crud.get_all_books(session)
    return books


@router.get("/{slug}", response_model=BookSchema)
async def get_book_by_slug(
        slug: str, session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    book = await crud.get_book_by_slug(slug, session)
    return book


@router.get("/{book_id}", response_model=BookSchema)
async def get_book_by_id(
        book_id: int, session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    book = await crud.get_book_by_id(book_id, session)
    return book


@router.delete("/{book_id}")
async def delete_book_by_id(
        book_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    success = await crud.delete_book(session, book_id)
    if success:
        return {"message": f"The book with id {book_id} has been deleted"}
    else:
        return {"message": "Deleting Error"}