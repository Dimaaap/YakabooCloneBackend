from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from admin.cities.schema import CitiesListForAdmin
from core.models import City


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