import json
import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from..books.crud import BASE_FILTER
from ..books.services import BookFilter
from core.models import DoubleSubcategory, Book, db_helper
from ..double_subcategories.schema import DoubleSubcategorySchema, DoubleSubcategoryCreate


async def create_double_subcategory(
        session: AsyncSession,
        double_subcategory: DoubleSubcategoryCreate
) -> DoubleSubcategory:
    new_double_subcategory = DoubleSubcategory(**double_subcategory.model_dump())

    try:
        session.add(new_double_subcategory)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return new_double_subcategory


async def get_all_double_subcategories(session: AsyncSession) -> list[DoubleSubcategorySchema]:
    statement = select(DoubleSubcategory).order_by(DoubleSubcategory.id)

    result: Result = await session.execute(statement)
    double_subcategories = result.scalars().all()
    return double_subcategories


async def get_double_subcategory_by_slug(session: AsyncSession, slug: str) -> DoubleSubcategory:
    statement = select(DoubleSubcategory).where(DoubleSubcategory.slug == slug, DoubleSubcategory.is_visible)
    
    result: Result = await session.execute(statement)
    double_subcategory = result.scalars().first()

    if not double_subcategory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Double subcategory with slug '{slug}' not found")
    return double_subcategory


async def delete_double_subcategory_by_id(session: AsyncSession, double_subcategory_id: int):
    statement = delete(DoubleSubcategory).where(DoubleSubcategory.id == double_subcategory_id)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        return False


async def get_all_double_subcategory_books_by_double_subcategory_id(session: AsyncSession, double_subcategory_id: int):
    statement = (
        select(Book)
        .join(Book.double_subcategories)
        .where(DoubleSubcategory.id == double_subcategory_id)
        .options(
            selectinload(Book.images),
            joinedload(Book.publishing),
            joinedload(Book.book_info)
        )
    )

    result: Result = await session.execute(statement)
    books = result.unique().scalars().all()
    return books or []


async def get_all_double_subcategory_books_by_double_subcategory_slug(session: AsyncSession,
                                                                      double_subcategory_slug: str, limit: int,
                                                                      offset: int, filter):

    base_query = (
        select(Book)
        .join(Book.double_subcategories)
        .where(BASE_FILTER, DoubleSubcategory.slug == double_subcategory_slug)
    )

    bf = BookFilter(filter)
    conditions = bf.apply()

    if conditions:
        base_query = base_query.where(and_(*conditions))

    total_statement = select(func.count()).select_from(base_query.subquery())
    total = await session.scalar(total_statement)

    statement = (
        base_query
        .options(
            selectinload(Book.images),
            joinedload(Book.publishing),
            joinedload(Book.book_info)
        )
        .offset(offset)
        .limit(limit)
    )

    result: Result = await session.execute(statement)
    books = result.unique().scalars().all()
    return books, total


async def main():
    with open("subcategories.json", "r", encoding="utf-8") as f:
        subcategories = json.load(f)

    async with db_helper.session_factory() as session:
        for subcategory in subcategories:
            subcat = DoubleSubcategoryCreate(**subcategory)
            await create_double_subcategory(session, subcat)


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())



