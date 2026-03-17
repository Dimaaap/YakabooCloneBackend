from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from admin.authors.errors import NotFoundInDbError
from admin.book_info.crud import get_book_info_list_for_admin_page
from admin.books.schema import BooksForAdminList, EditBook, CreateBook
from core.models import Book, Author, BookTranslator, BookIllustrator, Category, Subcategory, DoubleSubcategory, \
    BookImage
from entities.notebook_categories.views import get_all_notebook_categories
from entities.notebook_subcategories.crud import get_all_notebook_subcategories
from .forms import BookCreateForm
from ..authors.crud import get_authors_list_for_admin_page
from ..book_illustrators.crud import get_book_illustrator_for_admin_page
from ..book_series.crud import get_book_series_for_admin_page
from ..book_translators.crud import get_book_translators_for_admin_page
from ..category.crud import get_categories_for_admin_page
from ..double_subcategories.crud import get_double_subcategories_for_admin_page
from ..literatute_periods.crud import get_literature_periods_for_admin_page
from ..publishing.crud import get_publishing_list_for_admin_page


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


async def get_book_by_id(session: AsyncSession, book_id: int) -> Book | bool:
    book = await session.get(Book, book_id)

    if not book:
        return False
    return book


async def update_book(session: AsyncSession, book_id: int,
                      data: EditBook) -> bool:
    book = await get_book_by_id(session, book_id)

    if not book:
        raise NotFoundInDbError("Book not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(book, field, value)

    await session.commit()
    await session.refresh(book)
    return True


async def create_book(session: AsyncSession, data: CreateBook) -> Book | bool:
    book = Book(
        title=data.title,
        slug=data.slug,
        price=data.price,
        is_top=data.is_top,
        is_promo=data.is_promo,
        is_in_chart=data.is_in_chart,
        promo_price=data.promo_price,
        is_notebook=data.is_notebook,
        book_info_id=data.book_info_id,
        literature_period_id=data.literature_period_id,
        seria_id=data.seria_id,
        publishing_id=data.publishing_id,
        edition_group_id=data.edition_group_id,
        notebook_category_id=data.notebook_category_id,
        notebook_subcategory_id=data.notebook_subcategory_id,
    )

    session.add(book)

    m2m_model_field_map = {
        Author: ("authors", data.authors_ids),
        BookTranslator: ("translators", data.translators_ids),
        BookIllustrator: ("illustrators", data.illustrators_ids),
        Category: ("categories", data.categories_ids),
        Subcategory: ("subcategories", data.subcategories_ids),
        DoubleSubcategory: ("double_subcategories", data.double_subcategories_ids),
        BookImage: ("images", data.book_images_ids),

    }

    for model, (field, ids) in m2m_model_field_map.items():
        await set_m2m(session, book, field, model, ids)

    await session.commit()
    await session.refresh(book)
    return book


async def set_m2m(session: AsyncSession, book: Book, field_name: str, model, ids: list[int] | None):
    if ids:
        result = await session.execute(
            select(model).where(model.id.in_(ids))
        )
        result = result.scalars().all()
        setattr(book, field_name, result)
    else:
        setattr(book, field_name, [])
        return


class FieldsSetter:
    def __init__(self, session: AsyncSession, form):
        self.__form = form
        self.__session = session

    async def set_book_info_in_form_options(self):
        book_info_data = await get_book_info_list_for_admin_page(self.__session)
        choices = [(0, "---")] + [(info.id, info.id) for info in book_info_data]
        self.__form.book_info_id.choices = choices

    async def set_authors_in_form_options(self):
        authors = await get_authors_list_for_admin_page(self.__session)
        choices = [(author.id, f"{author.first_name} {author.last_name}") for author in authors]
        self.__form.author_ids.choices = choices

    async def set_translators_in_form_options(self):
        translators = await get_book_translators_for_admin_page(self.__session)
        choices = [(t.id, f"{t.first_name} {t.last_name}") for t in translators]
        self.__form.translators_ids.choices = choices

    async def set_illustrators_in_form_options(self):
        illustrators = await get_book_illustrator_for_admin_page(self.__session)
        choices = [(i.id, f"{i.first_name} {i.last_name}") for i in illustrators]
        self.__form.illustrators_ids.choices = choices

    async def set_book_seria_in_form_options(self):
        book_series = await get_book_series_for_admin_page(self.__session)
        choices = [(0, "---")] + [(s.id, s.title) for s in book_series]
        self.__form.seria_id.choices = choices

    async def set_categories_in_form_options(self):
        categories = await get_categories_for_admin_page(self.__session)
        choices = [(cat.id, cat.title) for cat in categories]
        self.__form.categories_ids.choices = choices

    async def set_double_subcategories_in_form_options(self):
        double_subcategories = await get_double_subcategories_for_admin_page(self.__session)
        choices = [(d.id, d.title) for d in double_subcategories]
        self.__form.double_subcategories_ids.choices = choices

    async def set_publishing_in_form_options(self):
        publishing = await get_publishing_list_for_admin_page(self.__session)
        choices = [(0, "---")] + [(p.id, p.title) for p in publishing]
        self.__form.publishing_id.choices = choices

    async def set_literature_periods_in_form_options(self):
        periods = await get_literature_periods_for_admin_page(self.__session)
        choices = [(0, "---")] + [(p.id, p.title) for p in periods]
        self.__form.literature_period_id.choices = choices

    async def main(self):
        for attr_name in dir(self):
            if attr_name.startswith("set_") and callable(getattr(self, attr_name)):
                await getattr(self, attr_name)()
