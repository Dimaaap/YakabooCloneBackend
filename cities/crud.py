import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession

from cities.schemas import CitiesSchema, CitiesCreate
from core.models import City, db_helper
from data_strorage import CITIES


async def create_city(session: AsyncSession, city: CitiesCreate) -> City:
    new_city = City(**city.model_dump())
    try:
        session.add(new_city)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return new_city


async def get_all_cities(session: AsyncSession) -> list[CitiesSchema]:
    statement = select(City).order_by(City.id).where(City.is_visible)
    result: Result = await session.execute(statement)
    cities = result.scalars().all()
    return [CitiesSchema.model_validate(city) for city in cities]


async def get_city_by_id(city_id: int, session: AsyncSession) -> CitiesSchema:
    statement = select(City).where(City.id == city_id)
    result: Result = await session.execute(statement)
    city = result.scalars().first()
    return CitiesSchema.model_validate(city)


async def delete_city_by_id(city_id: int, session: AsyncSession):
    statement = delete(City).where(City.id == city_id)
    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False


async def main():
    async with db_helper.session_factory() as session:
        for city in CITIES:
            city = CitiesCreate(**city)
            await create_city(session, city)


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())