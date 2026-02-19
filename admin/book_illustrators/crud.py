from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.book_illustrators.schema import BookIllustratorsListForAdmin
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