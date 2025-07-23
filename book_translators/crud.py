import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete, func, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import BookTranslator, db_helper, Book
from book_translators.schemas import BookTranslatorSchema, BookTranslatorCreate
from data_strorage import TRANSLATORS


async def create_translator(
        session: AsyncSession,
        translator: BookTranslatorCreate,
) -> BookTranslator:
    new_translator = BookTranslator(**translator.model_dump())
    try:
        session.add(new_translator)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return new_translator


async def get_all_translators(session: AsyncSession) -> list[BookTranslatorSchema]:
    statement = select(BookTranslator).order_by(BookTranslator.id)
    result: Result = await session.execute(statement)
    translators = result.scalars().all()
    return [BookTranslatorSchema.model_validate(translator) for translator in translators]

async def get_translators_by_query(query: str, session: AsyncSession):
    query = query.strip()
    similarity_first = func.similarity(BookTranslator.first_name, query)
    similarity_last = func.similarity(BookTranslator.last_name, query)

    statement = (
        select(BookTranslator)
        .where(
            or_(
                similarity_first > -0.1,
                similarity_last > 0.1,
                BookTranslator.first_name.like(f"%{query}%"),
                BookTranslator.last_name.like(f"%{query}%"),
            )
        )
        .order_by(func.greatest(similarity_first, similarity_last).desc())
    )

    result: Result = await session.execute(statement)
    translators = result.scalars().all()
    return list(translators) if translators else []


async def get_translator_by_slug(slug: str, session: AsyncSession) -> BookTranslator:
    statement = (select(BookTranslator)
                 .where(BookTranslator.slug == slug, BookTranslator.is_active))
    result: Result = await session.execute(statement)
    translator = result.scalars().first()
    
    if not translator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detailt=f"Translator with slug {slug} was not found")
    return translator


async def delete_translator_by_id(session: AsyncSession, translator_id: int):
    statement = delete(BookTranslator).where(BookTranslator.id == translator_id)
    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False

async def get_all_translator_books_by_translator_id(session: AsyncSession, translator_id: int):
    statement = (
        select(Book)
        .join(Book.translators)
        .where(BookTranslator.id == translator_id)
        .options(
            selectinload(Book.book_info),
            selectinload(Book.translators),
            selectinload(Book.subcategories),
            selectinload(Book.publishing),
            selectinload(Book.images)
        )
    )
    
    result: Result = await session.execute(statement)
    books = result.unique().scalars().all()
    if not books: 
        return []
    return books


async def main():
    async with db_helper.session_factory() as session:
        for translator in TRANSLATORS:
            await create_translator(session=session,
                                    translator=BookTranslatorCreate.model_validate(translator))
    return "Done"


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())