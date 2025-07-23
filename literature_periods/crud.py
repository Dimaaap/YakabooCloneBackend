import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import LiteraturePeriods, db_helper, Book
from literature_periods.schemas import LiteraturePeriodSchema, LiteraturePeriodCreate


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