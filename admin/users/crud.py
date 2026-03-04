from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.users.schema import UserListForAdmin, UserUpdate
from core.models import User, UserSeenBook


async def get_users_list_for_admin_page(session: AsyncSession) -> list[UserListForAdmin]:
    statement = (
        select(User)
        .options(
            selectinload(User.reviews),
            selectinload(User.orders),
            selectinload(User.seen_books).joinedload(UserSeenBook.book)
        )
        .order_by(User.id))
    result = await session.execute(statement)
    users = result.scalars().all()

    for user in users:
        user.reviews_text = [review.comment for review in user.reviews] if user.reviews else None
        user.orders_id = [order.id for order in user.orders] if user.orders else None
        user.seen_books_title = [book.book.title for book in user.seen_books] if user.seen_books else None

    return [
        UserListForAdmin.model_validate(user)
        for user in users
    ]


async def get_user_field_data(session: AsyncSession, user_id: int) -> UserListForAdmin:
    statement = (
        select(User)
        .options(
            selectinload(User.reviews),
            selectinload(User.orders),
            selectinload(User.seen_books).joinedload(UserSeenBook.book)
        )
        .where(User.id == user_id)
        .order_by(User.id)
    )

    result = await session.execute(statement)
    user = result.scalars().first()

    user.reviews_text = [review.comment for review in user.reviews] if user.reviews else None
    user.orders_id = [order.id for order in user.orders] if user.orders else None
    user.seen_books_title = [book.book.title for book in user.seen_books] if user.seen_books else None

    return UserListForAdmin.model_validate(user)


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | bool:
    user = await session.get(User, user_id)

    if not user:
        return False
    return user


async def update_user(session: AsyncSession, user_id: int,
                      data: UserUpdate) -> bool:
    user = await get_user_by_id(session, user_id)

    if not user:
        raise NotFoundInDbError("User not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(user, field, value)

    await session.commit()
    return True