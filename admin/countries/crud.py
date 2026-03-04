from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.countries.schema import CountriesListForAdmin, EditCountry
from core.models import Country


async def get_countries_list_for_admin_page(session: AsyncSession) -> list[CountriesListForAdmin]:
    statement = select(Country).order_by(Country.id)
    result = await session.execute(statement)
    countries = result.scalars().all()

    return [
        CountriesListForAdmin.model_validate(country)
        for country in countries
    ]


async def get_country_field_data(session: AsyncSession, country_id: int) -> CountriesListForAdmin:
    statement = (
        select(Country)
        .where(Country.id == country_id)
    )

    result = await session.execute(statement)
    country = result.scalars().first()

    return CountriesListForAdmin.model_validate(country)


async def get_country_by_id(session: AsyncSession, country_id: int) -> Country | bool:
    country = await session.get(Country, country_id)

    if not country:
        return False

    return country


async def update_country(session: AsyncSession, country_id: int, data: EditCountry) -> bool:
    country = await get_country_by_id(session, country_id)

    if not country:
        raise NotFoundInDbError("Country not found")

    update_data = data.model_dump(exclude_uset=True)

    for field, value in update_data.items():
        setattr(country, field, value)

    await session.commit()

    return True