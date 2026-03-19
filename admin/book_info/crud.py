from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from admin.authors.errors import NotFoundInDbError
from admin.book_info.schema import BookInfoListForAdmin, EditBookInfo, CreateBookInfo
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
        info.book_title = info.book.title if info.book else None

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

    book_info.book_title = book_info.book.title if book_info.book else None

    return BookInfoListForAdmin.model_validate(book_info)


async def get_book_info_by_id(session: AsyncSession, book_info_id: int) -> BookInfo | bool:
    book_info = await session.get(BookInfo, book_info_id)

    if not book_info:
        return False
    return book_info


async def update_book_info(session: AsyncSession, book_info_id: int, data: EditBookInfo) -> bool:
    book_info = await get_book_info_by_id(session, book_info_id)

    if not book_info:
        raise NotFoundInDbError("Book info not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(book_info, field, value)

    await session.commit()
    await session.refresh(book_info)
    return True


async def create_book_info(session: AsyncSession, data: CreateBookInfo) -> BookInfo | bool:
    book_info = BookInfo(**data.model_dump())

    try:
        session.add(book_info)
        await session.commit()
        await session.refresh(book_info)
    except SQLAlchemyError:
        return False
    return book_info
