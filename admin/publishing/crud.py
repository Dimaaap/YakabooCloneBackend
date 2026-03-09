from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.publishing.schema import PublishingListForAdmin, EditPublishing
from core.models import Publishing


async def get_publishing_list_for_admin_page(session: AsyncSession) -> list[PublishingListForAdmin]:
    statement = (
        select(Publishing)
        .order_by(Publishing.id)
    )

    result = await session.execute(statement)
    publishing_list = result.scalars().all()

    return [
        PublishingListForAdmin.model_validate(publishing)
        for publishing in publishing_list
    ]


async def get_publishing_field_data(session: AsyncSession, publishing_id: int) -> PublishingListForAdmin:
    statement = (
        select(Publishing)
        .where(Publishing.id == publishing_id)
    )

    result = await session.execute(statement)
    publishing = result.scalars().first()

    return PublishingListForAdmin.model_validate(publishing)


async def get_publishing_by_id(session: AsyncSession, publishing_id: int) -> Publishing | bool:
    publishing = await session.get(Publishing, publishing_id)

    if not publishing:
        return False

    return publishing


async def update_publishing(session: AsyncSession, publishing_id: int, data: EditPublishing) -> bool:
    publishing = await get_publishing_by_id(session, publishing_id)

    if not publishing:
        raise NotFoundInDbError("Publishing not found")

    update_data = data.model_dump(exclude_uset=True)

    for field, value in update_data.items():
        setattr(publishing, field, value)

    await session.commit()

    return True