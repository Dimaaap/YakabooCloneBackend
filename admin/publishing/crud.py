from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.publishing.schema import PublishingListForAdmin
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