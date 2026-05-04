from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select, Result, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from entities.notifications.schema import NotificationSchema, NotificationCreate, NotificationUpdatePartial
from core.models import Notification, UserNotification


async def create_notification(session: AsyncSession, data: NotificationCreate,
                              user_ids: list[int] | None = None) -> Notification:
    new_notification = Notification(**data.model_dump())

    session.add(new_notification)
    await session.flush()

    if not data.is_global:
        if not user_ids:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user_ids required")

        session.add_all([
            UserNotification(
                user_id=user_id,
                notification_id=new_notification.id,
                is_read=False
            )
            for user_id in user_ids
        ])
    await session.commit()
    await session.refresh(new_notification)

    return new_notification


async def get_all_notifications(session: AsyncSession) -> list[NotificationSchema]:
    statement = select(Notification).order_by(Notification.id)
    result: Result = await session.execute(statement)
    notifications = result.scalars().all()
    return [NotificationSchema.model_validate(n) for n in notifications]


async def get_all_notifications_by_user_id(session: AsyncSession, user_id: int) -> list[NotificationSchema]:
    now = datetime.now(timezone.utc)

    statement = (
        select(Notification, UserNotification.is_read)
        .outerjoin(UserNotification,
                   and_(
                       UserNotification.notification_id == Notification.id,
                       UserNotification.user_id == user_id
                   )
                )
        .where(
            Notification.is_active == True,
            or_(
                Notification.is_global == True,
                UserNotification.user_id == user_id
            ),
            or_(
                Notification.expires_at.is_(None),
                Notification.expires_at > now
            )
        )
        .order_by(Notification.created_at.desc())
    )

    result = await session.execute(statement)
    rows = result.all()

    return [
        NotificationSchema
        .model_validate(notif)
        .model_copy(
            update={"is_read": is_read if is_read is not None else False}
        )
        for notif, is_read in rows
    ]


async def get_unread_notifications_by_user_id(session: AsyncSession, user_id: int) -> list[NotificationSchema]:
    now = datetime.now(timezone.utc)

    read_subquery = (
        select(UserNotification.notification_id)
        .where(
            UserNotification.user_id == user_id,
            UserNotification.is_read == True
        )
        .subquery()
    )

    statement = (
        select(Notification)
        .where(
            Notification.is_active == True,
            or_(
                Notification.is_global == True,
                Notification.id.in_(
                    select(UserNotification.notification_id).where(
                        UserNotification.user_id == user_id
                    )
                )
            ),
            ~Notification.id.in_(select(read_subquery)),
            or_(
                Notification.expires_at.is_(None),
                Notification.expires_at > now
            )
        )
        .order_by(Notification.created_at.desc())
    )

    result = await session.execute(statement)
    notifications = result.scalars().all()

    return [
        NotificationSchema
        .model_validate(notif)
        .model_copy(update={"is_read": False})
        for notif in notifications
    ]


async def mark_notification_as_read(session: AsyncSession, user_id: int, notification_ids: list[int]) -> None:
    statement = select(UserNotification).where(
        UserNotification.user_id == user_id,
        UserNotification.notification_id.in_(notification_ids)
    )

    result = await session.execute(statement)
    existing = result.scalars().all()
    existing_ids = {n.notification_id for n in existing}

    for row in existing:
        row.is_read = True

    missing_ids = set(notification_ids) - existing_ids

    session.add_all([
        UserNotification(
            user_id=user_id,
            notification_id=n_id,
            is_read=True
        )
        for n_id in missing_ids
    ])

    await session.commit()


async def mark_all_notifications_as_read(session: AsyncSession, user_id: int) -> None:
    statement = select(Notification.id).outerjoin(
        UserNotification,
        and_(
            UserNotification.notification_id == Notification.id,
            UserNotification.user_id == user_id
        )
    ).where(
        Notification.is_active == True,
        or_(
            Notification.is_global == True,
            UserNotification.user_id == user_id
        )
    )

    result = await session.execute(statement)
    notification_ids = result.scalars().all()

    if not notification_ids:
        return

    statement_existing = select(UserNotification).where(
        UserNotification.user_id == user_id,
        UserNotification.notification_id.in_(notification_ids)
    )

    result_existing = await session.execute(statement_existing)
    existing = result_existing.scalars().all()

    existing_ids = {n.notification_id for n in existing}

    for row in existing:
        row.is_read = True

    missing_ids = set(notification_ids) - existing_ids
    session.add_all([
        UserNotification(
            user_id=user_id,
            notification_id=n_id,
            is_read=True
        )
        for n_id in missing_ids
    ])

    await session.commit()



async def delete_notification_global(session: AsyncSession, notification_id: int) -> bool | None:
    notification = await session.get(Notification, notification_id)

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    await session.delete(notification)
    await session.commit()
    return True


async def update_notification(session: AsyncSession, notification_id: int,
                              data: NotificationUpdatePartial) -> Notification:
    notification = await session.get(Notification, notification_id)

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(notification, key, value)

    await session.commit()
    await session.refresh(notification)
    return notification

