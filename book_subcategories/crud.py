import json
import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from books.crud import BASE_FILTER
from books.services import BookFilter
from core.models import Subcategory, Book, db_helper, Author, DoubleSubcategory
from book_subcategories.schema import BookSubcategorySchema, BookSubcategoryCreate


async def create_subcategory(
        session: AsyncSession,
        subcategory: BookSubcategoryCreate
) -> Subcategory:
    new_subcategory = Subcategory(**subcategory.model_dump())
    try:
        session.add(new_subcategory)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return new_subcategory


async def get_all_subcategories(session: AsyncSession) -> list[BookSubcategorySchema]:
    statement=(select(Subcategory)
               .options(selectinload(Subcategory.double_subcategories))
               .order_by(Subcategory.id))

    result: Result = await session.execute(statement)
    subcategories = result.scalars().all()
    return subcategories


async def get_subcategory_by_slug(slug: str, session: AsyncSession) -> Subcategory:
    statement = (
        select(Subcategory)
        .options(selectinload(Subcategory.double_subcategories))
        .where(Subcategory.slug == slug, Subcategory.is_visible)
    )

    result: Result = await session.execute(statement)
    subcategory = result.scalars().first()

    if not subcategory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subcategory not found")
    return subcategory


async def delete_subcategory_by_id(session: AsyncSession, subcategory_id: int):
    statement = delete(Subcategory).where(Subcategory.id == subcategory_id)
    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        return False


async def get_all_double_subcategories_by_subcategory_id(session: AsyncSession,
                                                         subcategory_id: int) -> list[DoubleSubcategory]:
    statement = (select(DoubleSubcategory).where(DoubleSubcategory.subcategory_id == subcategory_id)
                 .order_by(DoubleSubcategory.title))

    try:
        result: Result = await session.execute(statement)
        double_subcategories = result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return double_subcategories or []


async def get_all_subcategory_books_by_subcategory_id(session: AsyncSession, subcategory_id: int):
    statement = (
        select(Book)
        .join(Book.subcategories)
        .where(Subcategory.id == subcategory_id)
        .options(
            selectinload(Book.authors).joinedload(Author.interesting_fact),
            selectinload(Book.authors).selectinload(Author.images),
            selectinload(Book.images),
            joinedload(Book.publishing),
            joinedload(Book.book_info),

        )
    )

    result: Result = await session.execute(statement)
    books = result.unique().scalars().all()
    return books or []


async def get_all_subcategory_books_by_subcategory_slug(session: AsyncSession, subcategory_slug: str, limit: int,
                                                        offset: int, filter):
    base_query = (
        select(Book).join(Book.subcategories).where(BASE_FILTER, Subcategory.slug == subcategory_slug)
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
            selectinload(Book.authors).joinedload(Author.interesting_fact),
            selectinload(Book.authors).selectinload(Author.images),
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
            subcat = BookSubcategoryCreate(**subcategory)
            await create_subcategory(session, subcat)


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())


