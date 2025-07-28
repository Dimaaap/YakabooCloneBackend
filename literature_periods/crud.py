import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, aliased

from core.models import LiteraturePeriods, db_helper, Book
from literature_periods.schemas import LiteraturePeriodSchema, LiteraturePeriodCreate, LiteraturePeriodWithCountSchema
from data_strorage import LITERATURE_PERIODS


async def create_literature_period(
        session: AsyncSession,
        literature_period: LiteraturePeriodCreate
) -> LiteraturePeriodSchema:
    period = LiteraturePeriods(**literature_period.model_dump())

    try:
        session.add(period)
        await session.commit()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return period


async def get_literature_period_by_book_id(session: AsyncSession,
                                           book_id: int):
    statement = (
        select(LiteraturePeriods)
        .join(LiteraturePeriods.books)
        .where(Book.id == book_id)
    )

    result: Result = await session.execute(statement)
    literature_period = result.scalars().first()

    if not literature_period:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Literature for book with id {book_id} was not found"
        )

    return LiteraturePeriodSchema.model_validate(literature_period)


async def get_all_literature_periods(session: AsyncSession) -> list[LiteraturePeriodSchema]:
    statement = select(LiteraturePeriods).order_by(LiteraturePeriods.id)

    result: Result = await session.execute(statement)
    literature_periods = result.scalars().all()
    return [LiteraturePeriodSchema.model_validate(period) for period in literature_periods]


async def get_literature_period_by_slug(session: AsyncSession, slug: str):
    statement = (
        select(LiteraturePeriods)
        .where(LiteraturePeriods.slug == slug)
        .options(
            selectinload(LiteraturePeriods.books)
            .selectinload(Book.book_info),
            selectinload(LiteraturePeriods.books)
            .selectinload(Book.translators),
            selectinload(LiteraturePeriods.books)
            .selectinload(Book.subcategories),
            selectinload(LiteraturePeriods.books)
            .selectinload(Book.publishing),
            selectinload(LiteraturePeriods.books)
            .selectinload(Book.images),
        )
    )

    result: Result = await session.execute(statement)
    literature_period = result.scalars().first()


    if not literature_period:
        return []
    return literature_period


async def get_literature_period_by_id(session: AsyncSession, literature_period_id: int) -> LiteraturePeriodSchema:
    statement = select(LiteraturePeriods).where(LiteraturePeriods.id == literature_period_id)

    result: Result = await session.execute(statement)
    literature_period = result.unique().scalars().first()

    if not literature_period:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Literature period with id {literature_period_id} was not found")
    return literature_period


async def get_literature_periods_by_query(query: str, session: AsyncSession):
    query = query.strip()
    similarity = func.similarity(LiteraturePeriods.title, query)

    statement = (
        select(LiteraturePeriods)
        .where(
            or_(
                similarity > 0.1,
                LiteraturePeriods.title.like(f"%{query}%")
            )
        )
        .order_by(similarity.desc())
    )

    result: Result = await session.execute(statement)
    periods = result.scalars().all()
    return list(periods) if periods else []


async def get_all_period_books_by_period_id(session: AsyncSession, period_id: int):
    statement = (
        select(Book)
        .join(Book.literature_period)
        .where(Book.literature_period_id == period_id)
        .options(
            selectinload(Book.book_info),
            selectinload(Book.translators),
            selectinload(Book.subcategories),
            selectinload(Book.literature_period),
            selectinload(Book.publishing),
            selectinload(Book.images)
        )
    )

    result: Result = await session.execute(statement)
    books = result.unique().scalars().all()

    if not books:
        return []
    return books


async def delete_literature_period_by_id(session: AsyncSession, literature_period_id: int):

    statement = delete(LiteraturePeriods).where(LiteraturePeriods.id == literature_period_id)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False


async def get_books_count_by_literature_period(session: AsyncSession):
    BookAlias = aliased(Book)

    statement = (
        select(
            LiteraturePeriods.id,
            LiteraturePeriods.title,
            LiteraturePeriods.slug,
            func.count(BookAlias.id).label("books_count")
        )
        .outerjoin(BookAlias, LiteraturePeriods.id == BookAlias.literature_period_id)
        .group_by(LiteraturePeriods.id)
        .order_by(LiteraturePeriods.id)
    )

    result = await session.execute(statement)
    data = result.all()
    return [
        {
            "id": row.id,
            "title": row.title,
            "slug": row.slug,
            "books_count": row.books_count or 0
        }
        for row in data if row is not None
    ]

async def main():
    async with db_helper.session_factory() as session:
        for period in LITERATURE_PERIODS:
            period = LiteraturePeriodCreate(**period)
            await create_literature_period(session, period)


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
