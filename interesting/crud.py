import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Interesting, db_helper
from interesting.schemas import InterestingCreate, InterestingSchema
from data_strorage import INTERESTING


async def create_interesting(session: AsyncSession, interesting: InterestingCreate) -> Interesting:
    interesting = Interesting(**interesting.model_dump())
    try:
        session.add(interesting)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return interesting


async def delete_interesting_by_id(session: AsyncSession, interesting_id: int):
    statement = delete(Interesting).where(Interesting.id == interesting_id)
    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        await session.rollback()
        return False


async def get_all_interesting(session: AsyncSession) -> list[InterestingSchema]:
    statement = select(Interesting).order_by(Interesting.id).where(Interesting.visible)
    result: Result = await session.execute(statement)
    interesting = result.scalars().all()
    return [InterestingSchema.model_validate(interest) for interest in interesting]


async def main():
    async with db_helper.session_factory() as session:
        for interest in INTERESTING:
            await create_interesting(session, InterestingCreate.model_validate(interest))


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())