from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.sidebar.schema import SidebarsForAdminPage, EditSidebar
from core.models import Sidebar


async def get_sidebars_list_for_admin_page(session: AsyncSession) -> list[SidebarsForAdminPage]:
    statement = select(Sidebar).order_by(Sidebar.id)

    result = await session.execute(statement)
    sidebars = result.scalars().all()

    return [
        SidebarsForAdminPage.model_validate(sidebar)
        for sidebar in sidebars
    ]


async def get_sidebars_field_data(session: AsyncSession, sidebar_id: int) -> SidebarsForAdminPage:
    statement = (
        select(Sidebar)
        .where(Sidebar.id == sidebar_id)
    )

    result = await session.execute(statement)
    sidebar = result.scalars().first()

    return SidebarsForAdminPage.model_validate(sidebar)


async def get_sidebar_by_id(session: AsyncSession, sidebar_id: int) -> Sidebar | bool:
    sidebar = await session.get(Sidebar, sidebar_id)

    if not sidebar:
        return False

    return sidebar


async def update_sidebar(session: AsyncSession, sidebar_id: int, data: EditSidebar) -> bool:
    sidebar = await get_sidebar_by_id(session, sidebar_id)

    if not sidebar:
        raise NotFoundInDbError("Sidebar not found")

    update_data = data.model_dump(exclude_uset=True)

    for field, value in update_data.items():
        setattr(sidebar, field, value)

    await session.commit()

    return True