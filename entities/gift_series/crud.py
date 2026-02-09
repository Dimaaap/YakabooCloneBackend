import asyncio

from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import GiftSeries, db_helper, Gift
from data_strorage import GIFT_SERIES
from ..gift_series.schemas import GiftSeriaSchema, GiftSeriaCreate


async def create_gift_seria(
        session: AsyncSession,
        seria: GiftSeriaCreate
) -> GiftSeries:
    new_seria = GiftSeries(**seria.model_dump())

    if seria.gifts:
        statement = select(Gift).where(Gift.id.in_(seria.gifts))
        result = await session.execute(statement)
        gifts = result.scalars().all()

        for gift in gifts:
            gift.seria = new_seria
    session.add(new_seria)
    await session.commit()
    await session.refresh(new_seria)
    return new_seria


async def get_all_series(session: AsyncSession) -> list[GiftSeriaSchema]:
    statement = select(GiftSeries).options(selectinload(GiftSeries.gifts)).order_by(GiftSeries.id)
    result: Result = await session.execute(statement)
    series = result.scalars().all()
    return [GiftSeriaSchema.model_validate(seria) for seria in series]


async def delete_seria_by_id(seria_id: int, session: AsyncSession):
    statement = delete(GiftSeries).where(GiftSeries.id == seria_id)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False


async def get_seria_by_slug(seria_slug: str, session: AsyncSession) -> GiftSeries:
    statement = select(GiftSeries).where(GiftSeries.slug == seria_slug)
    result: Result = await session.execute(statement)
    series = result.scalars().first()
    return series


async def get_seria_by_id(seria_id: int, session: AsyncSession) -> GiftSeries:
    statement = select(GiftSeries).where(GiftSeries.id == seria_id)
    result: Result = await session.execute(statement)
    series = result.scalars().first()
    return series


async def main():
    async with db_helper.session_factory() as session:
        for seria in GIFT_SERIES:
            seria = GiftSeriaCreate(**seria)
            await create_gift_seria(session, seria)


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())