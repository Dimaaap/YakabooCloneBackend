from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.users.schema import UserListForAdmin
from core.models import User


async def get_users_list_for_admin_page(session: AsyncSession) -> list[UserListForAdmin]:
    statement = select(User).order_by(User.id)
    result = await session.execute(statement)
    users = result.scalars().all()

    return [
        UserListForAdmin.model_validate(user)
        for user in users
    ]
