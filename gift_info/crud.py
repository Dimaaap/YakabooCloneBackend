import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import GiftInfo, db_helper
from data_strorage import GIFTS_INFO
from gift_info.schemas import GiftInfoSchema, GiftInfoCreate


async def create_gift_info(
        session: AsyncSession,
        gift_info: GiftInfoCreate,
) -> GiftInfoSchema:
    gift_info = GiftInfo(**gift_info.model_dump())

    try:
        session.add(gift_info)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return gift_info


async def get_gift_info_by_gift_id(session: AsyncSession, gift_id: int):
    statement = (
        select(GiftInfo)
        .join(GiftInfo.gift)
        .where(GiftInfo.gift.has(id=gift_id))
    )

    result: Result = await session.execute(statement)
    gift_info = result.scalars().first()

    if not gift_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"GiftInfo for book with id={gift_id} not found",
        )

    return GiftInfoSchema.model_validate(gift_info)


async def get_all_gift_info(session: AsyncSession):
    statement = select(GiftInfo).order_by(GiftInfo.id)

    result: Result = await session.execute(statement)
    gift_info = result.scalars().all()
    return gift_info


async def main():
    async with db_helper.session_factory() as session:
        for gift_info in GIFTS_INFO:
            await create_gift_info(session, GiftInfoCreate.model_validate(gift_info))


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())