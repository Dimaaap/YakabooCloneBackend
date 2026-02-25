from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.ukrpost_office.schema import UkrpostOfficesForAdmin
from core.models import UkrpostOffice


async def get_ukrpost_offices_for_admin_page(session: AsyncSession) -> list[UkrpostOfficesForAdmin]:
    statement = (
        select(UkrpostOffice)
        .options(joinedload(UkrpostOffice.city))
        .order_by(UkrpostOffice.id)
    )

    results = await session.execute(statement)
    offices = results.scalars().all()

    for office in offices:
        office.city_title = office.city.title

    return [
        UkrpostOfficesForAdmin.model_validate(office)
        for office in offices
    ]