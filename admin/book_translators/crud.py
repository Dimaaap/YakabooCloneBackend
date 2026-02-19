from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.book_translators.schema import BookTranslatorsListForAdminPage
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