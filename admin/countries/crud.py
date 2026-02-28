from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.countries.schema import CountriesListForAdmin
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