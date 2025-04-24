import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Sidebar, db_helper
from data_strorage import SIDEBAR
from sidebar.schemas import Sidebar as SchemasSidebar


async def create_sidebar(session: AsyncSession, title: str,
                         slug: str, icon: str, visible: bool, order_number: int = 1,
                         is_clickable: bool = False) -> SchemasSidebar:
    sidebar = Sidebar(title=title, slug=slug, icon=icon, visible=visible, order_number=order_number,
                      is_clickable=is_clickable)
    try:
        session.add(sidebar)
        await session.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return sidebar


async def delete_sidebar_by_id(sidebar_id: int,
                               session: AsyncSession):
    statement = delete(Sidebar).where(Sidebar.id == sidebar_id)
    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False


async def get_all_sidebars(session: AsyncSession) -> list[SchemasSidebar]:
    statement = select(Sidebar).order_by(Sidebar.order_number, Sidebar.id)
    result: Result = await session.execute(statement)
    sidebars = result.scalars().all()
    return [SchemasSidebar.model_validate(sidebar) for sidebar in sidebars]


async def main():
    async with db_helper.session_factory() as session:
        for sidebar in SIDEBAR:
            await create_sidebar(session, title=sidebar["title"], slug=sidebar["slug"],
                                 icon=sidebar.get("icon", ""), visible=sidebar.get("visible", True),
                                 order_number=sidebar.get("order_number", 1),
                                 is_clickable=sidebar.get("is_clickable", True))


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())