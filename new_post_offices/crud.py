import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession

from new_post_offices.schema import NewPostOfficeSchema, NewPostOfficeCreate
from core.models import NewPostOffice, db_helper
from new_post_postomats.services import convert_json_offices_format


async def create_new_post_office(session: AsyncSession, office: NewPostOfficeCreate) -> NewPostOffice:
    new_office = NewPostOffice(**office.model_dump())

    try:
        session.add(new_office)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return new_office


async def get_all_new_post_offices(session: AsyncSession) -> list[NewPostOfficeSchema]:
    statement = select(NewPostOffice).where(NewPostOffice.active).order_by(NewPostOffice.id)

    result: Result = await session.execute(statement)
    offices = result.scalars().all()
    return [NewPostOfficeSchema.model_validate(office) for office in offices]


async def get_office_by_id(office_id: int, session: AsyncSession) -> NewPostOffice:
    statement = select(NewPostOffice).where(NewPostOffice.id == office_id, NewPostOffice.active)

    result: Result = await session.execute(statement)
    office = result.scalars().first()
    return office


async def get_new_post_office_by_city_id(city_id: int, session: AsyncSession) -> list[NewPostOffice]:
    statement = (
        select(NewPostOffice)
        .where(NewPostOffice.city_id == city_id, NewPostOffice.active)
        .order_by(NewPostOffice.id)
    )

    result: Result = await session.execute(statement)
    new_post_offices = result.scalars().all()
    return new_post_offices


async def delete_new_post_office_by_id(office_id: int, session: AsyncSession) -> bool:
    statement = delete(NewPostOffice).where(NewPostOffice.id == office_id)

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
            await create_new_post_office(session, NewPostOfficeCreate.model_validate(office))

if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())