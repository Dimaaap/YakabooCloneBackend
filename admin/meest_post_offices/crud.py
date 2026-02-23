from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.meest_post_offices.schema import MeestPostOfficesForAdmin
from core.models import MeestPostOffice


async def get_meest_post_offices_for_admin_page(session: AsyncSession) -> list[MeestPostOfficesForAdmin]:
    statement = (
        select(MeestPostOffice)
        .options(joinedload(MeestPostOffice.city))
        .order_by(MeestPostOffice.id))

    result = await session.execute(statement)
    offices = result.scalars().all()

    for office in offices:
        office.city_title = office.city.title

    return [
        MeestPostOfficesForAdmin.model_validate(office)
        for office in offices
    ]
