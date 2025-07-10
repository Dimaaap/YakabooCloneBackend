import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import BookInfo, db_helper
from book_info.schemas import BookInfoSchema, BookInfoCreate
from data_strorage import BOOKS_INFO


async def create_book_info(
        session: AsyncSession,
        book_info: BookInfoCreate
) -> BookInfoSchema:
    book_info = BookInfo(**book_info.model_dump())

    try:
        session.add(book_info)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return book_info


async def get_book_info_by_book_id(session: AsyncSession,
                                   book_id: int):
    statement = (
        select(BookInfo)
        .join(BookInfo.book)
        .where(BookInfo.book.has(id=book_id))
    )

    result: Result = await session.execute(statement)
    book_info = result.scalars().first()

    if not book_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"BookInfo for book with id={book_id} not found"
        )

    return BookInfoSchema.model_validate(book_info)


async def get_all_books_info(session: AsyncSession):
    statement = select(BookInfo).order_by(BookInfo.id)

    result: Result = await session.execute(statement)
    book_info = result.scalars().all()
    return book_info


async def main():
    async with db_helper.session_factory() as session:
        for book_info in BOOKS_INFO:
            await create_book_info(session, BookInfoCreate.model_validate(book_info))


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())