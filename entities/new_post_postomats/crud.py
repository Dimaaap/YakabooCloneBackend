import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession

from ..new_post_postomats.schema import NewPostPostomatSchema, NewPostPostomatCreate
from core.models import NewPostPostomat, db_helper
from ..new_post_postomats.services import convert_json_postomats_format


async def create_new_post_postomat(session: AsyncSession, postomat: NewPostPostomatCreate) -> NewPostPostomat:
    new_postomat = NewPostPostomat(**postomat.model_dump())

    try:
        session.add(new_postomat)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return new_postomat


async def get_all_new_post_postomats(session: AsyncSession) -> list[NewPostPostomatSchema]:
    statement = select(NewPostPostomat).where(NewPostPostomat.active).order_by(NewPostPostomat.id)

    result: Result = await session.execute(statement)
    postomats = result.scalars().all()
    return [NewPostPostomatSchema.model_validate(postomat) for postomat in postomats]


async def get_postomat_by_id(postomat_id: int, session: AsyncSession) -> NewPostPostomat:
    statement = select(NewPostPostomat).where(NewPostPostomat.id == postomat_id, NewPostPostomat.active)

    result: Result = await session.execute(statement)
    postomat = result.scalars().first()
    return postomat


async def get_new_post_postomats_by_city_id(city_id: int, session: AsyncSession) -> list[NewPostPostomat]:
    statement = (
        select(NewPostPostomat)
        .where(NewPostPostomat.city_id == city_id, NewPostPostomat.active)
        .order_by(NewPostPostomat.id)
    )
    result: Result = await session.execute(statement)
    new_post_postomats = result.scalars().all()
    return new_post_postomats


async def delete_new_post_postomat_by_id(postomat_id: int, session: AsyncSession) -> bool:
    statement = delete(NewPostPostomat).where(NewPostPostomat.id == postomat_id)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False


async def main():
    postomats = convert_json_postomats_format()
    async with db_helper.session_factory() as session:
        for index, postomat in enumerate(postomats):
            print(index)
            postomat["id"] = index + 1
            await create_new_post_postomat(session, NewPostPostomatCreate.model_validate(postomat))


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())