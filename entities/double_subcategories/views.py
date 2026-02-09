from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from entities.books.schemas import BookFilters
from .schema import DoubleSubcategorySchema, DoubleSubcategoryCreate
from core.models import db_helper
from . import crud

router = APIRouter(tags=["Book Double Subcategories"])


@router.get("/all", response_model=list[DoubleSubcategorySchema])
async def get_all_double_subcategories(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    double_subcategories = await crud.get_all_double_subcategories(session)
    return double_subcategories


@router.get("/{slug}", response_model=DoubleSubcategorySchema)
async def get_double_subcategory_by_slug(
        slug: str, session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_double_subcategory_by_slug(session, slug)


@router.post("/create")
async def create_double_subcategory(
        double_subcategory: DoubleSubcategoryCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    new_double_subcategory = await crud.create_double_subcategory(session, double_subcategory)
    if new_double_subcategory:
        return new_double_subcategory
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(new_double_subcategory))


@router.delete("/{double_subcategory_id}")
async def delete_double_subcategory_by_id(subcategory_id: int,
                                          session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    success = await delete_double_subcategory_by_id(subcategory_id, session)

    if success:
        return {"message": f"Book double subcategory {subcategory_id} was deleted"}
    return {"message": "Deleting Error"}


@router.get("/double_subcategory/{double_subcategory_id}/books")
async def get_all_double_subcategory_books_by_double_subcategory_id(
        double_subcategory_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    books = await crud.get_all_double_subcategory_books_by_double_subcategory_id(session, double_subcategory_id)

    return books


@router.get("/double_subcategory/by-slug/{double_subcategory_slug}/books")
async def get_all_double_subcategory_books_by_double_subcategory_slug(
        double_subcategory_slug: str,
        filter: BookFilters = Query(None),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    books, total = await crud.get_all_double_subcategory_books_by_double_subcategory_slug(
        session, double_subcategory_slug, limit=filter.limit, offset=filter.offset, filter=filter
    )
    return {
        "count": total,
        "limit": filter.limit,
        "offset": filter.offset,
        "has_more": filter.offset + filter.limit < total,
        "results": books
    }

