from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schema import NotificationCreate, NotificationUpdatePartial
from core.models import db_helper
from . import crud

router = APIRouter(tags=["notifications"])


@router.post("/create")
async def create_notification(
        data: NotificationCreate,
        user_ids: list[int] | None = None,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.create_notification(session, data, user_ids)


@router.get("/all")
async def get_all_notifications(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_all_notifications(session)


@router.get("/user/{user_id}")
async def get_all_notifications_for_user(
        user_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_all_notifications_by_user_id(session, user_id)


@router.get("/user/{user_id}/unread")
async def get_all_user_unread_notifications(
        user_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_unread_notifications_by_user_id(session, user_id)


@router.post("/{notification_id}/read")
async def mark_as_read(
        notification_id: int,
        user_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    await crud.mark_notification_as_read(session, user_id, [notification_id])
    return {"success": True}


@router.post("/read")
async def mark_multiple_as_read_view(
        notification_ids: list[int],
        user_id: int,
        session: AsyncSession=Depends(db_helper.scoped_session_dependency)
):
    await crud.mark_notification_as_read(session, user_id, notification_ids)
    return {"success": True}


@router.post("user/{user_id}/read-all")
async def mark_all_as_read(
        user_id: int,
        session: AsyncSession=Depends(db_helper.scoped_session_dependency)
):
    await crud.mark_all_notifications_as_read(session, user_id)
    return {"success": True}


@router.delete("/{notification_id}")
async def delete_notification_view(
        notification_id: int,
        session: AsyncSession=Depends(db_helper.scoped_session_dependency)
):
    await crud.delete_notification_global(session, notification_id)
    return {"status": "deleted"}


@router.patch("/{notification_id}")
async def update_notification(
        notification_id: int,
        data: NotificationUpdatePartial,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.update_notification(session, notification_id, data)



