import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import GiftSubCategory, db_helper, Gift, BoardGameAge
from data_strorage import GIFT_SUBCATEGORIES
from entities.gift_subcategories.schemas import GiftSubcategorySchema, GiftSubcategoryCreate


async def create_gift_subcategory(
        session: AsyncSession,
        gift_subcategory: GiftSubcategoryCreate,
) -> GiftSubcategorySchema:
    subcategory = GiftSubCategory(**gift_subcategory.model_dump())

    try:
        session.add(subcategory)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return subcategory


async def get_all_gift_subcategories(session: AsyncSession) -> list[GiftSubcategorySchema]:
    statement = select(GiftSubCategory).order_by(GiftSubCategory.id)

    result: Result = await session.execute(statement)
    gift_subcategories = result.scalars().all()
    return [GiftSubcategorySchema.model_validate(subcategory) for subcategory in gift_subcategories]


async def get_gift_subcategory_by_slug(session: AsyncSession, slug: str):
    statement = select(GiftSubCategory).where(GiftSubCategory.slug == slug)

    result: Result = await session.execute(statement)
    gift_subcategory = result.scalars().first()

    return gift_subcategory or []


async def get_gifts_by_subcategory_slug(session: AsyncSession, subcategory_slug: str):
    statement = (
        select(GiftSubCategory)
        .where(GiftSubCategory.slug == subcategory_slug)
        .options(
            selectinload(GiftSubCategory.gifts).joinedload(Gift.brand),
            selectinload(GiftSubCategory.gifts).selectinload(Gift.ages).selectinload(BoardGameAge.board_game),
            selectinload(GiftSubCategory.gifts).joinedload(Gift.seria),
            selectinload(GiftSubCategory.gifts).selectinload(Gift.images),
        )
    )

    result: Result = await session.execute(statement)
    subcategory = result.scalars().first()
    return subcategory


async def get_gift_subcategory_by_id(session: AsyncSession, subcategory_id: int) -> GiftSubcategorySchema:
    statement = select(GiftSubCategory).where(GiftSubCategory.id == subcategory_id)

    result: Result = await session.execute(statement)
    subcategory = result.scalars().first()

    return subcategory or []


async def delete_gift_subcategory_by_id(session: AsyncSession, subcategory_id: int):
    statement = delete(GiftSubCategory).where(GiftSubCategory.id == subcategory_id)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False


async def main():
    async with db_helper.session_factory() as session:
        for subcategory in GIFT_SUBCATEGORIES:
            await create_gift_subcategory(session, GiftSubcategoryCreate.model_validate(subcategory))


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

