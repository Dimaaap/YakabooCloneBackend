from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from admin.book_info.schema import BookInfoListForAdmin
from core.models import BookInfo


async def get_book_info_list_for_admin_page(session: AsyncSession) -> list[BookInfoListForAdmin]:
    statement = (
        select(BookInfo)
        .options(joinedload(BookInfo.book))
        .order_by(BookInfo.id)
    )

    result = await session.execute(statement)
    book_info_list = result.unique().scalars().all()

    for info in book_info_list:
        info.book_title = info.book.title

    return [
        BookInfoListForAdmin.model_validate(info)
        for info in book_info_list
    ]


async def get_book_info_field_data(session: AsyncSession, book_info_id: int) -> BookInfoListForAdmin:
    statement = (
        select(BookInfo)
        .options(joinedload(BookInfo.book))
        .where(BookInfo.id == book_info_id)
    )

    result = await session.execute(statement)
    book_info = result.scalars().first()

    book_info.book_title = book_info.book.title

    return BookInfoListForAdmin.model_validate(book_info)