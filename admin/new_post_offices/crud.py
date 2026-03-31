from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.cities.crud import get_cities_list_for_admin_page
from admin.new_post_offices.schema import NewPostOfficesForAdmin, EditNewPostOffice, CreateNewPostOffice
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


async def get_new_post_offices_field_data(session: AsyncSession, office_id: int) -> NewPostOfficesForAdmin:
    statement = (
        select(NewPostOffice)
        .options(joinedload(NewPostOffice.city))
        .where(NewPostOffice.id == office_id)
    )

    result = await session.execute(statement)
    office = result.scalars().first()

    office.city_title = office.city.title
    return NewPostOfficesForAdmin.model_validate(office)


async def get_new_post_office_by_id(session: AsyncSession, office_id: int) -> NewPostOffice | bool:
    office = await session.get(NewPostOffice, office_id)

    if not office:
        return False

    return office


async def update_new_post_office(session: AsyncSession, office_id: int, data: EditNewPostOffice) -> bool:
    office = await get_new_post_office_by_id(session, office_id)

    if not office:
        raise NotFoundInDbError("New Post Office not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(office, field, value)

    await session.commit()
    await session.refresh(office)
    return True


async def create_new_post_office(session: AsyncSession, data: CreateNewPostOffice) -> NewPostOffice | bool:
    office = NewPostOffice(**data.model_dump())

    try:
        session.add(office)
        await session.commit()
        await session.refresh(office)
    except SQLAlchemyError:
        return False
    return office


async def set_cities_in_choices(session: AsyncSession, form) -> None:
    cities = await get_cities_list_for_admin_page(session)
    choices = [(city.id, city.title) for city in cities]
    form.city_id.choices = choices