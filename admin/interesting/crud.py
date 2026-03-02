from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.interesting.schema import InterestingForAdminList
from core.models import Interesting


async def get_interesting_list_for_admin_page(session: AsyncSession) -> list[InterestingForAdminList]:
    statement = select(Interesting).order_by(Interesting.id)
    result = await session.execute(statement)
    interesting_list = result.scalars().all()

    return [
        InterestingForAdminList.model_validate(interesting)
        for interesting in interesting_list
    ]


async def get_interesting_field_data(session: AsyncSession, interesting_id: int) -> InterestingForAdminList:
    statement = (
        select(Interesting)
        .where(Interesting.id == interesting_id)
    )

    result = await session.execute(statement)
    interesting = result.scalars().first()

    return InterestingForAdminList.model_validate(interesting)