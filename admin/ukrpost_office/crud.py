from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.ukrpost_office.schema import UkrpostOfficesForAdmin, EditUkrpostOffice
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


async def get_ukrpost_offices_field_data(session: AsyncSession, office_id: int) -> UkrpostOfficesForAdmin:
    statement = (
        select(UkrpostOffice)
        .options(joinedload(UkrpostOffice.city))
        .where(UkrpostOffice.id == office_id)
    )

    result = await session.execute(statement)
    office = result.scalars().first()

    office.city_title = office.city.title
    return UkrpostOfficesForAdmin.model_validate(office)



async def get_ukrpost_office_by_id(session: AsyncSession, office_id: int) -> UkrpostOffice | bool:
    office = await session.get(UkrpostOffice, office_id)

    if not office:
        return False

    return office


async def update_ukrpost_office(session: AsyncSession, office_id: int, data: EditUkrpostOffice) -> bool:
    office = await get_ukrpost_office_by_id(session, office_id)

    if not office:
        raise NotFoundInDbError("Ukrpost Office not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(office, field, value)

    await session.commit()
    await session.refresh(office)
    return True