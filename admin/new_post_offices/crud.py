from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.new_post_offices.schema import NewPostOfficesForAdmin
from core.models import NewPostOffice


async def get_new_post_offices_for_admin_page(session: AsyncSession) -> list[NewPostOfficesForAdmin]:
    statement = (
        select(NewPostOffice)
        .options(joinedload(NewPostOffice.city))
        .order_by(NewPostOffice.id)
    )

    result = await session.execute(statement)
    offices = result.scalars().all()

    for office in offices:
        office.city_title = office.city.title

    return [
        NewPostOfficesForAdmin.model_validate(office)
        for office in offices
    ]