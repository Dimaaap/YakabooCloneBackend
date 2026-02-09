import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from entities.countries.schemas import CountriesSchema, CountriesCreate
from core.models import Country, db_helper, City
from data_strorage import COUNTRIES


async def create_country(session: AsyncSession, country: CountriesCreate) -> Country:
    new_country = Country(**country.model_dump())
    try:
        session.add(new_country)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return new_country


async def get_all_countries(session: AsyncSession) -> list[CountriesSchema]:
    statement = (select(Country).order_by(Country.id)
                 .where(Country.is_visible)
                 .options(selectinload(Country.cities)
                          .selectinload(City.delivery_terms),
                          selectinload(Country.cities).selectinload(City.payment_methods),
                          selectinload(Country.delivery_terms),
                          selectinload(Country.payment_methods)
                          )
                 )
    result: Result = await session.execute(statement)
    countries = result.scalars().all()
    return [CountriesSchema.model_validate(country) for country in countries]


async def get_country_by_id(country_id: int, session: AsyncSession) -> CountriesSchema:
    statement = (select(Country)
                 .where(Country.id == country_id)
                 .options(selectinload(Country.cities)
                          .selectinload(City.delivery_terms),
                          selectinload(Country.cities).selectinload(City.payment_methods),
                          selectinload(Country.delivery_terms),
                          selectinload(Country.payment_methods)
                          )
                 )
    result: Result = await session.execute(statement)
    country = result.scalars().first()
    return CountriesSchema.model_validate(country)


async def get_country_by_title(country_title: str, session: AsyncSession) -> CountriesSchema:
    statement = (select(Country)
                 .where(Country.title == country_title)
                 .options(selectinload(Country.cities)
                          .selectinload(Country.delivery_terms),
                          selectinload(Country.cities).selectinload(City.payment_methods),
                          selectinload(Country.delivery_terms),
                          selectinload(Country.payment_methods),
                          )
                 )
    result: Result = await session.execute(statement)
    country = result.scalars().first()
    return CountriesSchema.model_validate(country)


async def delete_country_by_id(country_id: int, session: AsyncSession):
    statement = delete(Country).where(Country.id == country_id)
    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False


async def main():
    async with db_helper.session_factory() as session:
        for country in COUNTRIES:
            new_country = CountriesCreate(**country)
            await create_country(session, new_country)


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())