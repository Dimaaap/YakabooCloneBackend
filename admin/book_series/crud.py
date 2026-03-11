from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.book_series.schema import BookSeriesForAdminList, EditBookSeria
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


async def get_book_seria_field_data(session: AsyncSession, seria_id: int) -> BookSeriesForAdminList:
    statement = (
        select(BookSeria)
        .where(BookSeria.id == seria_id)
    )

    result = await session.execute(statement)
    book_seria = result.scalars().first()

    return BookSeriesForAdminList.model_validate(book_seria)


async def get_book_seria_by_id(session: AsyncSession, seria_id: int) -> BookSeria | bool:
    book_seria = await session.get(BookSeria, seria_id)

    if not book_seria:
        return False

    return book_seria


async def update_book_seria(session: AsyncSession, seria_id: int, data: EditBookSeria) -> bool:
    book_seria = await get_book_seria_by_id(session, seria_id)

    if not book_seria:
        raise NotFoundInDbError("Book Seria not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(book_seria, field, value)

    await session.commit()
    await session.refresh(book_seria)
    return True