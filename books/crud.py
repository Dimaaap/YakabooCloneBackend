import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Book, db_helper, BookImage
from books.schemas import BookSchema, BookCreate, BookUpdate
from data_strorage import BOOKS


async def create_book(session: AsyncSession, book_data: BookCreate) -> BookSchema:
    book = Book(**book_data.model_dump(exclude="images"))

    for image_data in book_data.get("images", []):
        image = BookImage(image_url=image_data.image_url, type=image_data.type)
        book.images.append(image)

    try:
        session.add(book)
        await session.commit()
        await session.refresh(book)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return BookSchema.model_validate(book)


async def get_all_books(session: AsyncSession) -> list[BookSchema]:
    statement = (select(Book)
                 .options(
        joinedload(Book.book_info),
        selectinload(Book.authors),
        joinedload(Book.publishing),
        selectinload(Book.wishlists)
    ).order_by(Book.id))
    result: Result = await session.execute(statement)
    books = result.scalars().all()
    return [BookSchema.model_validate(book) for book in books]


async def get_book_by_id(book_id: int, session: AsyncSession) -> BookSchema:
    statement = (
        select(Book)
        .options(
            joinedload(Book.book_info),
            selectinload(Book.authors),
            joinedload(Book.publishing),
            selectinload(Book.wishlists)
        )
        .where(Book.id == book_id)
    )

    result: Result = await session.execute(statement)
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The book with id {book_id} was not found")
    return BookSchema.model_validate(book)


async def get_book_by_slug(slug: str, session: AsyncSession) -> BookSchema:
    statement = (
        select(Book)
        .options(joinedload(Book.book_info))
        .where(Book.slug == slug)
    )

    result: Result = await session.execute(statement)
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The book with slug {slug} was not found")
    return BookSchema.model_validate(book)


async def update_book(session: AsyncSession, book_id: int, book_data: BookUpdate) -> BookSchema:
    book = await session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    for key, value in book_data.model_dump(exclude_unset=True).items():
        setattr(book, key, value)

    try:
        await session.commit()
        await session.refresh(book)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return BookSchema.model_validate(book)


async def delete_book(session: AsyncSession, book_id: int) -> bool:
    statement = delete(Book).where(Book.id == book_id)
    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(f"Error deleting book: {e}")
        await session.rollback()
        return False


async def main():
    async with db_helper.session_factory() as session:
        for book in BOOKS:
            await create_book(session, BookCreate.model_validate(book))


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())