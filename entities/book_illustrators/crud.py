from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete, func, or_, and_
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from entities.books.services import BookFilter
from core.models import Book, BookIllustrator
from entities.book_illustrators.schemas import BookIllustratorSchema, BookIllustratorCreate
from entities.publishing.crud import BASE_FILTER


async def create_illustrator(
        session: AsyncSession,
        illustrator: BookIllustratorCreate,
) -> BookIllustrator:
    new_illustrator = BookIllustrator(**illustrator.model_dump())
    try:
        session.add(new_illustrator)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return new_illustrator


async def get_all_illustrators(session: AsyncSession) -> list[BookIllustratorSchema]:
    statement = select(BookIllustrator).order_by(BookIllustrator.id)
    result: Result = await session.execute(statement)
    illustrators = result.scalars().all()
    return [BookIllustratorSchema.model_validate(illustrator) for illustrator in illustrators]


async def get_illustrator_by_query(query: str, session: AsyncSession):
    query = query.strip()
    similarity_first = func.similarity(BookIllustrator.first_name, query)
    similarity_last = func.similarity(BookIllustrator.last_name, query)

    statement = (
        select(BookIllustrator)
        .where(
            or_(
                similarity_first > 0.1,
                similarity_last > 0.1,
                BookIllustrator.first_name.like(f"%{query}%"),
                BookIllustrator.last_name.like(f"%{query}%")
            )
        )
        .order_by(func.greatest(similarity_first, similarity_last).desc())
    )

    result: Result = await session.execute(statement)
    illustrators = result.scalars().all()
    return list(illustrators) if illustrators else []


async def get_illustrator_by_slug(session: AsyncSession, slug: str) -> BookIllustrator:
    statement = (
        select(BookIllustrator)
        .where(BookIllustrator.slug == slug, BookIllustrator.is_active)
    )
    result: Result = await session.execute(statement)
    illustrator = result.scalars().first()

    if not illustrator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Illustrator with slug {slug} was not found")
    return illustrator


async def delete_illustrator_by_id(session: AsyncSession, illustrator_id: int):
    statement = delete(BookIllustrator).where(BookIllustrator.id == illustrator_id)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        return False


async def get_all_illustrator_books_by_illustrator_id(session: AsyncSession, illustrator_id: int,
                                                      limit: int, offset: int, filter):
    # statement = (
    #     select(Book)
    #     .join(Book.illustrators)
    #     .where(BookIllustrator.id == illustrator_id)
    #     .options(
    #         joinedload(Book.book_info),
    #         selectinload(Book.translators),
    #         selectinload(Book.illustrators),
    #         joinedload(Book.publishing),
    #         selectinload(Book.images),
    #         selectinload(Book.literature_period),
    #         joinedload(Book.seria)
    #     )
    # )

    base_query = (
        select(Book)
        .join(Book.illustrators)
        .where(BASE_FILTER, BookIllustrator.id == illustrator_id)
    )

    bf = BookFilter(filter)
    conditions = bf.apply()

    if conditions:
        base_query = base_query.where(and_(*conditions))

    total_statement = select(func.count()).select_from(base_query.subquery())
    total = await session.scalar(total_statement)

    statement = (
        base_query
        .options(
            joinedload(Book.book_info),
            selectinload(Book.translators),
            selectinload(Book.illustrators),
            joinedload(Book.publishing),
            selectinload(Book.images),
            selectinload(Book.literature_period),
            joinedload(Book.seria)
        )
    )

    result: Result = await session.execute(statement)
    books = result.unique().scalars().all()
    if not books:
        return []

    return books, total
