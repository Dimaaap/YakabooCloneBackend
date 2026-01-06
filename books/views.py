from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import BookSchema, BookCreate, PaginatedBookSchema, BookFilters
from core.models import db_helper
from . import crud

router = APIRouter(tags=["books"])

@router.get('/all', response_model=PaginatedBookSchema)
async def get_all_books(
        filter: BookFilters = Query(None),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    books, total = await crud.get_all_books(session=session, limit=filter.limit, offset=filter.offset,
                                            filters=filter)
    return {
        "count": total,
        "limit": filter.limit,
        "offset": filter.offset,
        "has_more": filter.offset + filter.limit < total,
        "results": books
    }


@router.get('/notebooks/all', response_model=list[BookSchema])
async def get_all_notebooks(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    notebooks = await crud.get_all_notebooks(session)
    return notebooks


@router.get("/{slug}", response_model=BookSchema)
async def get_book_by_slug(
        slug: str, session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    book = await crud.get_book_by_slug(slug, session)
    return book


@router.get('/notebook/{notebook_slug}', response_model=BookSchema)
async def get_notebook_by_slug(
        notebook_slug: str, session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    notebook = await crud.get_notebook_by_slug(notebook_slug, session)
    return notebook


@router.get("/by-id/{book_id}", response_model=BookSchema)
async def get_book_by_id(
        book_id: int, session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    book = await crud.get_book_by_id(book_id, session)
    return book


@router.get('/notebook/{notebook_id}')
async def get_notebook_by_id(
        notebook_id: int, session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    notebook = await crud.get_notebook_by_id(notebook_id, session)
    return notebook


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