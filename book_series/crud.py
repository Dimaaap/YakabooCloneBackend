import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete, func, or_
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import BookSeria, db_helper, Book
from book_series.schema import BookSeriaSchema, BookSeriaCreate


async def create_seria(
        session: AsyncSession,
        seria: BookSeriaCreate,
) -> BookSeria:
    new_seria = BookSeria(**seria.model_dump())
    try:
        session.add(new_seria)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return new_seria


async def get_all_series(session: AsyncSession) -> list[BookSeriaSchema]:
    statement = (
        select(
            BookSeria,
            func.count(Book.id).label("books_count")
        )
        .outerjoin(Book, Book.seria_id == BookSeria.id)
        .group_by(BookSeria.id)
        .order_by(BookSeria.id)
    )

    result: Result = await session.execute(statement)
    rows = result.all()

    series_with_counts = [
        {
            **row.BookSeria.__dict__,
            "books_count": row.books_count
        }
        for row in rows
    ]

    return series_with_counts


async def get_series_by_query(query: str, session: AsyncSession):
    query = query.strip()
    similarity = func.similarity(BookSeria.title, query)

    statement = (
        select(BookSeria)
        .where(
            or_(
                similarity > 0.1,
                BookSeria.title.like(f"%{query}%")
            )
        )
        .order_by(similarity)
    )

    result: Result = await session.execute(statement)
    series = result.scalars().all()
    return list(series) if series else []


async def get_all_seria_books_by_seria_slug(session: AsyncSession, seria_slug: str):
    statement = (
        select(Book)
        .join(Book.seria)
        .where(BookSeria.slug == seria_slug)
        .options(
            selectinload(Book.book_info),
            selectinload(Book.translators),
            selectinload(Book.subcategories),
            selectinload(Book.publishing),
            selectinload(Book.images),
            selectinload(Book.literature_period),
            joinedload(Book.seria)
        )
    )

    result: Result = await session.execute(statement)
    books = result.unique().scalars().all()
    if not books:
        return []
    return books


async def get_seria_by_slug(slug: str, session: AsyncSession) -> BookSeria:
    statement = select(BookSeria).where(BookSeria.slug == slug, BookSeria.is_active)

    result: Result = await session.execute(statement)
    seria = result.scalars().first()

    if not seria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seria not found")
    return seria


async def delete_seria_by_id(session: AsyncSession, seria_id: int):
    statement = delete(BookSeria).where(BookSeria.id == seria_id)
    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        return False



async def main():
    async with db_helper.db_session() as session:
        ...


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())