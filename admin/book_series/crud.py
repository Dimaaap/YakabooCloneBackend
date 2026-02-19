from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.book_series.schema import BookSeriesForAdminList
from core.models import BookSeria


async def get_book_series_for_admin_page(session: AsyncSession) -> list[BookSeriesForAdminList]:
    statement = (
        select(BookSeria)
        .order_by(BookSeria.id)
    )

    result = await session.execute(statement)
    series = result.scalars().all()

    return [
        BookSeriesForAdminList.model_validate(seria)
        for seria in series
    ]