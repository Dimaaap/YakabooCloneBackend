from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.book_translators.schema import BookTranslatorsListForAdminPage, EditBookTranslator, CreateBookTranslator
from core.models import BookTranslator


async def get_book_translators_for_admin_page(session: AsyncSession) -> list[BookTranslatorsListForAdminPage]:
    statement = (
        select(BookTranslator)
        .order_by(BookTranslator.id)
    )

    result = await session.execute(statement)
    series = result.scalars().all()

    return [
        BookTranslatorsListForAdminPage.model_validate(seria)
        for seria in series
    ]


async def get_book_translator_field_data(session: AsyncSession, translator_id: int) -> BookTranslatorsListForAdminPage:
    statement = (
        select(BookTranslator)
        .where(BookTranslator.id == translator_id)
    )

    result = await session.execute(statement)
    book_translator = result.scalars().first()

    return BookTranslatorsListForAdminPage.model_validate(book_translator)


async def get_book_translator_by_id(session: AsyncSession, translator_id: int) -> BookTranslator | bool:
    book_translator = await session.get(BookTranslator, translator_id)

    if not book_translator:
        return False

    return book_translator


async def update_book_translator(session: AsyncSession, book_translator_id: int,
                                 data: EditBookTranslator) -> bool:
    book_translator = await get_book_translator_by_id(session, book_translator_id)

    if not book_translator:
        raise NotFoundInDbError("Book Translator not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(book_translator, field, value)

    await session.commit()
    await session.refresh(book_translator)
    return True


async def create_book_translator(session: AsyncSession, data: CreateBookTranslator) -> BookTranslator | bool:
    translator = BookTranslator(**data.model_dump())
    try:
        session.add(translator)
        await session.commit()
        await session.refresh(translator)
    except SQLAlchemyError:
        return False

    return translator