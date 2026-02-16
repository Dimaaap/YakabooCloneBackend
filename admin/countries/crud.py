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