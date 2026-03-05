from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.book_illustrators.schema import BookIllustratorsListForAdmin, EditBookIllustrator
from core.models import BookIllustrator, book


async def get_book_illustrator_for_admin_page(session: AsyncSession) -> list[BookIllustratorsListForAdmin]:

    statement = (
        select(BookIllustrator)
        .order_by(BookIllustrator.id)
    )

    result = await session.execute(statement)
    book_illustrators = result.scalars().all()

    return [
        BookIllustratorsListForAdmin.model_validate(illustrator)
        for illustrator in book_illustrators
    ]


async def get_book_illustrator_field_data(session: AsyncSession, illustrator_id: int) -> BookIllustratorsListForAdmin:
    statement = (
        select(BookIllustrator)
        .where(BookIllustrator.id == illustrator_id)
    )

    result = await session.execute(statement)
    book_illustrator = result.scalars().first()

    return BookIllustratorsListForAdmin.model_validate(book_illustrator)


async def get_book_illustrator_by_id(session: AsyncSession, illustrator_id: int) -> BookIllustrator | bool:
    book_illustrator = await session.get(BookIllustrator, illustrator_id)

    if not book_illustrator:
        return False
    return book_illustrator


async def update_book_illustrator(session: AsyncSession, book_illustrator_id: int,
                                  data: EditBookIllustrator) -> bool:
    book_illustrator = await get_book_illustrator_by_id(session, book_illustrator_id)

    if not book_illustrator:
        raise NotFoundInDbError("Author not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(book_illustrator, field, value)

    await session.commit()

    return True
