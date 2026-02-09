import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession

from entities.meest_post_offices.schema import MeestPostOfficeSchema, MeestPostOfficeCreate
from entities.meest_post_offices.services import convert_json_offices_format
from core.models import MeestPostOffice, db_helper


async def create_meest_office(session: AsyncSession, meest_office: MeestPostOfficeCreate) -> MeestPostOffice:
    new_office = MeestPostOffice(**meest_office.model_dump())

    try:
        session.add(new_office)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return new_office


async def get_all_meest_offices(session: AsyncSession) -> list[MeestPostOfficeSchema]:
    statement = select(MeestPostOffice).where(MeestPostOffice.active).order_by(MeestPostOffice.id)
    result: Result = await session.execute(statement)
    meest_offices = result.scalars().all()
    return [MeestPostOfficeSchema.model_validate(office) for office in meest_offices]


async def get_office_by_id(office_id: int, session: AsyncSession) -> MeestPostOffice:
    statement = select(MeestPostOffice).where(MeestPostOffice.id == office_id, MeestPostOffice.active)
    result: Result = await session.execute(statement)
    office = result.scalars().first()
    return office


async def get_meest_office_by_city_id(city_id: int, session: AsyncSession) -> list[MeestPostOffice]:
    statement = (
        select(MeestPostOffice)
        .where(MeestPostOffice.city_id == city_id, MeestPostOffice.active)
        .order_by(MeestPostOffice.id)
    )

    result: Result = await session.execute(statement)
    meest_offices = result.scalars().all()
    return meest_offices


async def delete_meest_office_by_id(office_id: int, session: AsyncSession) -> bool:
    statement = delete(MeestPostOffice).where(MeestPostOffice.id == office_id)

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
            await create_meest_office(session, MeestPostOfficeCreate.model_validate(office))


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
