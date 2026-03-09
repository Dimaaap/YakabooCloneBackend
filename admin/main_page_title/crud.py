from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.main_page_title.schema import MainPageTitlesListForAdmin, EditMainPageTitle
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


async def get_main_page_title_field_data(session: AsyncSession, main_page_title_id: int) -> MainPageTitlesListForAdmin:
    statement = (
        select(MainPageTitle)
        .where(MainPageTitle.id == main_page_title_id)
    )

    result = await session.execute(statement)
    main_page_title = result.scalars().first()

    return MainPageTitlesListForAdmin.model_validate(main_page_title)


async def get_main_page_title_by_id(session: AsyncSession, main_page_id: int) -> MainPageTitle | bool:
    title = await session.get(MainPageTitle, main_page_id)

    if not title:
        return False

    return title


async def update_main_page_title(session: AsyncSession, main_page_id: int, data: EditMainPageTitle) -> bool:
    title = await get_main_page_title_by_id(session, main_page_id)

    if not title:
        raise NotFoundInDbError("Main page title not found")

    update_data = data.model_dump(exclude_uset=True)

    for field, value in update_data.items():
        setattr(title, field, value)

    await session.commit()

    return True