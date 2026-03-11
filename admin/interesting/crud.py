from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.interesting.schema import InterestingForAdminList, EditInteresting
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


async def get_interesting_by_id(session: AsyncSession, interesting_id: int) -> Interesting | bool:
    interesting = await session.get(Interesting, interesting_id)

    if not interesting:
        return False

    return interesting


async def update_interesting(session: AsyncSession, interesting_id: int, data: EditInteresting) -> bool:
    interesting = await get_interesting_by_id(session, interesting_id)

    if not interesting:
        raise NotFoundInDbError("Interesting not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(interesting, field, value)

    await session.commit()
    await session.refresh(interesting)
    return True