from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from entities.books.schemas import BookFilters
from .schema import BookSubcategorySchema, BookSubcategoryCreate
from core.models import db_helper
from . import crud

router = APIRouter(tags=["Book Subcategories"])


@router.get('/all', response_model=list[BookSubcategorySchema])
async def get_all_subcategories(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    subcategories = await crud.get_all_subcategories(session)
    return subcategories


@router.get('/{slug}', response_model=BookSubcategorySchema)
async def get_subcategory_by_slug(
        slug: str, session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_subcategory_by_slug(slug, session)



@router.post("/create")
async def create_subcategory(
        subcategory: BookSubcategoryCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    new_subcategory = await crud.create_subcategory(session, subcategory)
    if new_subcategory:
        return new_subcategory
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detailt=str(new_subcategory))


@router.delete("/{subcategory_id}")
async def delete_subcategory_by_id(subcategory_id: int,
                                   session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    success = await crud.delete_subcategory_by_id(session, subcategory_id)
    if success:
        return {"message": f"Book subcategory with id {subcategory_id} was been deleted"}
    return {"message": "Deleting Error"}


@router.get("/subcategory/{subcategory_id}/books")
async def get_all_subcategory_books_by_subcategory_id(
        subcategory_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    books = await crud.get_all_subcategory_books_by_subcategory_id(session, subcategory_id)
    return books


@router.get("/subcategory/by-slug/{subcategory_slug}/books")
async def get_all_subcategory_books_by_subcategory_slug(
        subcategory_slug: str,
        filter: BookFilters = Query(None),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    books, total = await crud.get_all_subcategory_books_by_subcategory_slug(session, subcategory_slug,
                                                                            limit=filter.limit, offset=filter.offset,
                                                                            filter=filter)
    return {
        "count": total,
        "limit": filter.limit,
        "offset": filter.offset,
        "has_more": filter.offset + filter.limit < total,
        "results": books
    }


@router.get("/subcategory/double_subcategories/{subcategory_id}")
async def get_all_double_subcategories_by_subcategory_id(subcategory_id: int,
                                                         session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    double_subcategories = await crud.get_all_double_subcategories_by_subcategory_id(session, subcategory_id)
    return double_subcategories