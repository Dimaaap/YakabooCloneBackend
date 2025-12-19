import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Book, db_helper, BookImage, Author, BookTranslator
from books.schemas import BookSchema, BookCreate, BookUpdate
from data_strorage import BOOKS


async def create_book(session: AsyncSession, book_data: BookCreate) -> BookSchema:
    book = Book(**book_data.model_dump(exclude={"images", "authors", "translators"}))

    for image_data in book_data.images or []:
        image = BookImage(image_url=image_data.image_url, type=image_data.type)
        book.images.append(image)

    if book_data.authors:
        statement = select(Author).where(Author.id.in_(book_data.authors)).options(
            joinedload(Author.interesting_fact)
        )
        result = await session.execute(statement)
        authors = result.scalars().all()
        for author in authors:
            if author not in book.authors:
                book.authors.append(author)


    if book_data.translators:
        result = await session.execute(select(BookTranslator).where(BookTranslator.id.in_(book_data.translators)))
        translators = result.scalars().all()
        for translator in translators:
            if translator not in book.translators:
                book.translators.append(translator)

    try:
        session.add(book)
        await session.commit()
        await session.refresh(book, ["book_info", "authors", "publishing", "wishlists", "images",
                                     "translators", "literature_period", "notebook_category", "notebook_subcategory"])
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
            joinedload(Book.seria),
            selectinload(Book.images),
            joinedload(Book.edition_group),
            selectinload(Book.illustrators),
            selectinload(Book.reviews)
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
            joinedload(Book.seria),
            selectinload(Book.images),
            joinedload(Book.notebook_subcategory),
            joinedload(Book.notebook_category),
            joinedload(Book.edition_group),
            selectinload(Book.illustrators)
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
            selectinload(Book.authors).selectinload(Author.images),
            selectinload(Book.authors).joinedload(Author.interesting_fact),
            joinedload(Book.publishing),
            selectinload(Book.wishlists),
            joinedload(Book.seria),
            selectinload(Book.translators),
            joinedload(Book.literature_period),
            joinedload(Book.edition_group),
            selectinload(Book.illustrators),
            selectinload(Book.reviews)
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
            joinedload(Book.seria),
            selectinload(Book.translators),
            joinedload(Book.literature_period),
            selectinload(Book.illustrators),
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
            joinedload(Book.seria),
            joinedload(Book.literature_period),
            joinedload(Book.edition_group),
            selectinload(Book.illustrators),
            selectinload(Book.reviews)
        )
    )

    result: Result = await session.execute(statement)
    book = result.scalars().first()

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The book with slug {slug} was not found")
    related_books = []
    book_schema = BookSchema.model_validate(book)

    if book.edition_group_id:
        related_statement = (
            select(Book)
            .where(
                Book.edition_group_id == book.edition_group_id,
                Book.id != book.id,
            )
            .options(joinedload(Book.book_info))
        )
        related_result: Result = await session.execute(related_statement)
        related_books = related_result.unique().scalars().all()
        book_schema.related_books = [BookSchema.model_validate(book) for book in related_books]
    else:
        book_schema.related_books = []
    return book_schema


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
            joinedload(Book.seria),
            joinedload(Book.notebook_category),
            joinedload(Book.notebook_subcategory),
            selectinload(Book.illustrators)
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