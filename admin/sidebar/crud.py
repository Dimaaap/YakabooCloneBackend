from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.sidebar.schema import SidebarsForAdminPage
from core.models import Sidebar


async def get_sidebars_list_for_admin_page(session: AsyncSession) -> list[SidebarsForAdminPage]:
    statement = select(Sidebar).order_by(Sidebar.id)

    result = await session.execute(statement)
    sidebars = result.scalars().all()

    return [
        SidebarsForAdminPage.model_validate(sidebar)
        for sidebar in sidebars
    ]