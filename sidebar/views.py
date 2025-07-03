import json

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import Sidebar, SidebarCreate
from core.models import db_helper
from .import crud
from config import redis_client

router = APIRouter(tags=["sidebar"])

SIX_DAYS = 24 * 3600 * 6


@router.get("/all", response_model=list[Sidebar])
async def get_all_sidebars(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    cached_sidebars = await redis_client.get("sidebars")
    if cached_sidebars:
        return json.loads(cached_sidebars)
    sidebars = await crud.get_all_sidebars(session)
    await redis_client.set("sidebars", json.dumps([sidebar.model_dump() for sidebar in sidebars]),
                           ex=SIX_DAYS)

    print(sidebars)
    return sidebars


@router.post("/create")
async def create_sidebar(sidebar: SidebarCreate,
                         session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_sidebar = await crud.create_sidebar(session=session, title=sidebar.title,
                                            slug=sidebar.slug, icon=sidebar.icon,
                                            visible=sidebar.visible, order_number=sidebar.order_number,
                                            is_clickable=sidebar.is_clickable)
    if new_sidebar:
        await redis_client.delete("sidebars")
        return new_sidebar


@router.delete("/{sidebar_id}")
async def delete_sidebar_by_id(sidebar_id: int,
                               session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    deleted_sidebar = await crud.delete_sidebar_by_id(sidebar_id=sidebar_id, session=session)
    if deleted_sidebar:
        await redis_client.delete("sidebars")
        return {"message": f"The sidebar with id {sidebar_id} has been deleted"}
    else:
        return {"error": deleted_sidebar}