import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Book, db_helper, BookImage, Author
from books.schemas import BookSchema, BookCreate, BookUpdate
from data_strorage import BOOKS


async def create_book(session: AsyncSession, book_data: BookCreate) -> BookSchema:
    book = Book(**book_data.model_dump(exclude="images"))

    for image_data in book_data.images or []:
        image = BookImage(image_url=image_data.image_url, type=image_data.type)
        book.images.append(image)

    try:
        session.add(book)
        await session.commit()
        await session.refresh(book, ["book_info", "authors", "publishing", "wishlists", "images",
                                     "translators", "literature_period"])
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return BookSchema.model_validate(book)


async def get_all_books(session: AsyncSession) -> list[BookSchema]:
    statement = (
        select(Book)
        .where(Book.is_notebook == False)
        .options(
            joinedload(Book.book_info),
            selectinload(Book.authors).selectinload(Author.images),
            selectinload(Book.authors).joinedload(Author.interesting_fact),
            joinedload(Book.publishing),
            selectinload(Book.wishlists),
            selectinload(Book.translators),
            joinedload(Book.literature_period),
            selectinload(Book.images),
        )
        .order_by(Book.id))
    result: Result = await session.execute(statement)
    books = result.scalars().all()
    return [BookSchema.model_validate(book) for book in books]


async def get_all_notebooks(session: AsyncSession) -> list[BookSchema]:
    statement = (
        select(Book)
        .where(Book.is_notebook == True)
        .options(
            joinedload(Book.book_info),
            selectinload(Book.authors).selectinload(Author.images),
            selectinload(Book.authors).joinedload(Author.interesting_fact),
            joinedload(Book.publishing),
            selectinload(Book.wishlists),
            selectinload(Book.translators),
            joinedload(Book.literature_period),
            selectinload(Book.images),
        )
        .order_by(Book.id)
    )

    result: Result = await session.execute(statement)
    notebooks = result.scalars().all()
    return [BookSchema.model_validate(notebook) for notebook in notebooks]


async def get_book_by_id(book_id: int, session: AsyncSession) -> BookSchema:
    statement = (
        select(Book)
        .where(Book.is_notebook == False, Book.id == book_id)
        .options(
            joinedload(Book.book_info),
            selectinload(Book.authors),
            joinedload(Book.publishing),
            selectinload(Book.wishlists),
            selectinload(Book.translators),
            joinedload(Book.literature_period)
        )
    )

    result: Result = await session.execute(statement)
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The book with id {book_id} was not found")
    return BookSchema.model_validate(book)


async def get_notebook_by_id(notebook_id: int, session: AsyncSession) -> BookSchema:
    statement = (
        select(Book)
        .where(Book.is_notebook == True, Book.id == notebook_id)
        .options(
            joinedload(Book.book_info),
            selectinload(Book.authors),
            joinedload(Book.publishing),
            selectinload(Book.wishlists),
            selectinload(Book.translators),
            joinedload(Book.literature_period),
        )
    )

    result: Result = await session.execute(statement)
    notebook = result.scalars().first()
    if not notebook:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The notebook with id {notebook_id} was not found")
    return BookSchema.model_validate(notebook)


async def get_book_by_slug(slug: str, session: AsyncSession) -> BookSchema:
    statement = (
        select(Book)
        .where(Book.is_notebook == False, Book.slug == slug)
        .options(
            joinedload(Book.book_info),
            joinedload(Book.publishing),
            selectinload(Book.authors).selectinload(Author.interesting_fact),
            selectinload(Book.authors).selectinload(Author.images),
            selectinload(Book.images),
            joinedload(Book.literature_period),
            joinedload(Book.notebook_category),
            selectinload(Book.translators),
            joinedload(Book.literature_period),
        )
    )

    result: Result = await session.execute(statement)
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The book with slug {slug} was not found")
    return BookSchema.model_validate(book)


async def get_notebook_by_slug(notebook_slug: str, session: AsyncSession) -> BookSchema:
    statement = (
        select(Book)
        .where(Book.is_notebook == True, Book.slug == notebook_slug)
        .options(
            joinedload(Book.book_info),
            joinedload(Book.publishing),
            selectinload(Book.authors).selectinload(Author.interesting_fact),
            selectinload(Book.authors).selectinload(Author.images),
            selectinload(Book.images),
            selectinload(Book.translators),
            joinedload(Book.literature_period),
            joinedload(Book.notebook_category),
            joinedload(Book.notebook_subcategory)
        )
    )

    result: Result = await session.execute(statement)
    notebook = result.scalars().first()
    if not notebook:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The notebook with slug {notebook_slug} was not found")
    return BookSchema.model_validate(notebook)


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