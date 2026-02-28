from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from admin.books.schema import BooksForAdminList
from core.models import Book


async def get_books_for_admin_page(session: AsyncSession) -> list[BooksForAdminList]:
    statement = (
        select(Book)
        .options(
            joinedload(Book.book_info),
            selectinload(Book.authors),
            selectinload(Book.translators),
            selectinload(Book.illustrators),
            joinedload(Book.literature_period),
            joinedload(Book.seria),
            joinedload(Book.notebook_category),
            joinedload(Book.notebook_subcategory),
            selectinload(Book.categories),
            selectinload(Book.subcategories),
            selectinload(Book.double_subcategories),
            joinedload(Book.publishing),
            joinedload(Book.edition_group),
            selectinload(Book.images)
        )
        .order_by(Book.id)
    )

    result = await session.execute(statement)
    books = result.unique().scalars().all()

    for book in books:
        book.book_info_id = book.book_info.id
        book.authors_names = [f"{author.first_name} {author.last_name}"
                              for author in book.authors] if book.authors else None
        book.translators_names = [f"{translator.first_name} {translator.last_name}"
                                  for translator in book.translators] if book.translators else None
        book.illustrators_names = [f"{illustrator.first_name} {illustrator.last_name}"
                                   for illustrator in book.illustrators] if book.illustrators else None
        book.literature_period_title = book.literature_period.title if book.literature_period else None
        book.seria_title = book.seria.title if book.seria else None
        book.notebook_subcategory_title = book.notebook_subcategory.title if book.notebook_subcategory else None
        book.notebook_category_title = book.notebook_category.title if book.notebook_category else None
        book.categories_title = [category.title for category in book.categories] if book.categories else None
        book.subcategories_title = [subcategory.title for subcategory in
                                    book.subcategories] if book.subcategories else None
        book.double_subcategories_title = [double_subcategory.title
                                           for double_subcategory
                                           in book.double_subcategories] if book.double_subcategories else None
        book.publishing_title = book.publishing.title if book.publishing else None
        book.edition_group_title = book.edition_group.title if book.edition_group else None
        book.book_images = [image.image_url for image in book.images] if book.images else None


    return [
        BooksForAdminList.model_validate(book)
        for book in books
    ]


async def get_book_field_data(session: AsyncSession, book_id: int) -> BooksForAdminList:
    statement = (
        select(Book)
        .options(
            joinedload(Book.book_info),
            selectinload(Book.authors),
            selectinload(Book.translators),
            selectinload(Book.illustrators),
            joinedload(Book.literature_period),
            joinedload(Book.seria),
            joinedload(Book.notebook_category),
            joinedload(Book.notebook_subcategory),
            selectinload(Book.categories),
            selectinload(Book.subcategories),
            selectinload(Book.double_subcategories),
            joinedload(Book.publishing),
            joinedload(Book.edition_group),
            selectinload(Book.images)
        )
        .where(Book.id == book_id)
    )

    result = await session.execute(statement)
    book = result.scalars().first()

    book.book_info_id = book.book_info.id
    book.authors_names = [f"{author.first_name} {author.last_name}"
                          for author in book.authors] if book.authors else None
    book.translators_names = [f"{translator.first_name} {translator.last_name}"
                              for translator in book.translators] if book.translators else None
    book.illustrators_names = [f"{illustrator.first_name} {illustrator.last_name}"
                               for illustrator in book.illustrators] if book.illustrators else None
    book.literature_period_title = book.literature_period.title if book.literature_period else None
    book.seria_title = book.seria.title if book.seria else None
    book.notebook_subcategory_title = book.notebook_subcategory.title if book.notebook_subcategory else None
    book.notebook_category_title = book.notebook_category.title if book.notebook_category else None
    book.categories_title = [category.title for category in book.categories] if book.categories else None
    book.subcategories_title = [subcategory.title for subcategory in
                                book.subcategories] if book.subcategories else None
    book.double_subcategories_title = [double_subcategory.title
                                       for double_subcategory
                                       in book.double_subcategories] if book.double_subcategories else None
    book.publishing_title = book.publishing.title if book.publishing else None
    book.edition_group_title = book.edition_group.title if book.edition_group else None
    book.book_images = [image.image_url for image in book.images] if book.images else None

    return BooksForAdminList.model_validate(book)
