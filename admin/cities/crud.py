from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from admin.authors.errors import NotFoundInDbError
from admin.cities.schema import CitiesListForAdmin, EditCity, CreateCity
from core.models import City
from admin.countries.crud import get_countries_list_for_admin_page


async def get_cities_list_for_admin_page(session: AsyncSession) -> list[CitiesListForAdmin]:
    statement = (
        select(City)
        .options(selectinload(City.country))
        .order_by(City.id)
    )
    result = await session.execute(statement)
    cities = result.scalars().all()

    for city in cities:
        city.country_title = city.country.title

    return [
        CitiesListForAdmin.model_validate(city)
        for city in cities
    ]


async def get_city_field_data(session: AsyncSession, city_id: int) -> CitiesListForAdmin:
    statement = (
        select(City)
        .options(selectinload(City.country))
        .where(City.id == city_id)
    )

    result = await session.execute(statement)
    city = result.scalars().first()

    city.country_title = city.country.title

    return CitiesListForAdmin.model_validate(city)


async def get_city_by_id(session: AsyncSession, city_id: int) -> City | bool:
    city = await session.get(City, city_id)

    if not city:
        return False
    return city


async def update_city(session: AsyncSession, city_id: int, data: EditCity) -> bool:
    city = await get_city_by_id(session, city_id)

    if not city:
        raise NotFoundInDbError("City not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(city, field, value)

    await session.commit()
    await session.refresh(city)
    return True


async def create_city(session: AsyncSession, data: CreateCity) -> City | bool:
    city = City(**data.model_dump())
    try:
        session.add(city)
        await session.commit()
        await session.refresh(city)
    except SQLAlchemyError:
        return False
    return city


async def set_countries_in_choices(session: AsyncSession, form):
    countries = await get_countries_list_for_admin_page(session)
    choices = [(country.id, country.title) for country in countries]
    form.country_id.choices = choices