import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession

from ukrpost_offices.schema import UkrpostOfficeSchema, UkrpostOfficeCreate
from ukrpost_offices.services import convert_json_offices_format
from cities.crud import get_city_by_title
from core.models import UkrpostOffice, db_helper


async def create_ukrpost_office(session: AsyncSession, office: UkrpostOfficeCreate) -> UkrpostOffice:
    ukrpost_office = UkrpostOffice(**office.model_dump())
    try:
        session.add(ukrpost_office)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return ukrpost_office


async def get_all_ukrpost_offices(session: AsyncSession) -> list[UkrpostOfficeSchema]:
    statement = select(UkrpostOffice).where(UkrpostOffice.active).order_by(UkrpostOffice.id)
    result: Result = await session.execute(statement)
    ukrpost_offices = result.scalars().all()
    return [UkrpostOfficeSchema.model_validate(office) for office in ukrpost_offices]


async def get_office_by_id(office_id: int, session: AsyncSession) -> UkrpostOffice:
    statement = select(UkrpostOffice).where(UkrpostOffice.id == office_id, UkrpostOffice.active)
    result: Result = await session.execute(statement)
    office = result.scalars().first()
    return office


async def get_ukrpost_offices_by_city_id(city_id: int, session: AsyncSession) -> list[UkrpostOffice]:
    statement = (select(UkrpostOffice)
                 .where(UkrpostOffice.city_id == city_id, UkrpostOffice.active)
                 .order_by(UkrpostOffice.id))
    result: Result = await session.execute(statement)
    ukrpost_offices = result.scalars().all()
    return ukrpost_offices


async def delete_ukrpost_office_by_id(office_id: int, session: AsyncSession) -> bool:
    statement = delete(UkrpostOffice).where(UkrpostOffice.id == office_id)
    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False


async def main():
    offices = convert_json_offices_format()
    async with db_helper.session_factory() as session:
        for index, office in enumerate(offices):
            office["id"] = index + 1
            await create_ukrpost_office(session, UkrpostOfficeCreate.model_validate(office))


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())




