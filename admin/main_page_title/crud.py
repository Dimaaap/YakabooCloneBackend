from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.main_page_title.schema import MainPageTitlesListForAdmin
from core.models import MainPageTitle


async def get_main_page_titles_for_admin_page(session: AsyncSession) -> list[MainPageTitlesListForAdmin]:
    statement = (
        select(MainPageTitle)
        .order_by(MainPageTitle.id)
    )

    result = await session.execute(statement)
    main_page_titles = result.scalars().all()

    return [
        MainPageTitlesListForAdmin.model_validate(title)
        for title in main_page_titles
    ]