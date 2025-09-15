import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Gift, db_helper, GiftImage, BoardGameAge, GiftBrand, GiftSeries
from gifts.schemas import GiftSchema, GiftCreate, GiftUpdate
from data_strorage import GIFTS


async def create_gift(session: AsyncSession, gift_data: GiftCreate) -> GiftSchema:
    gift = Gift(**gift_data.model_dump(exclude={"images", "ages"}))

    for image_data in gift_data.images:
        image = GiftImage(image_url=image_data.image_url)
        gift.images.append(image)

    for age_id in gift_data.ages:
        age = await session.get(BoardGameAge, age_id)
        if age:
            gift.ages.append(age)

    try:
        session.add(gift)
        await session.commit()
        statement = (
            select(Gift).where(Gift.id == gift.id)
            .options(
                joinedload(Gift.brand).selectinload(GiftBrand.gifts),
                selectinload(Gift.ages).selectinload(BoardGameAge.board_game),
                joinedload(Gift.seria),
                selectinload(Gift.images),
                joinedload(Gift.gift_category),
                joinedload(Gift.gift_subcategory)
            )
        )

        result = await session.execute(statement)
        gift = result.scalars().first()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return GiftSchema.model_validate(gift)


async def get_all_gifts(session: AsyncSession) -> list[GiftSchema]:
    statement = (select(Gift)
                 .options(
                    joinedload(Gift.brand).selectinload(GiftBrand.gifts),
                    selectinload(Gift.ages).selectinload(BoardGameAge.board_game),
                    joinedload(Gift.seria).selectinload(GiftSeries.gifts),
                    selectinload(Gift.images),
                    joinedload(Gift.gift_category),
                    joinedload(Gift.gift_subcategory)
                )
                 .order_by(Gift.id)
            )
    result: Result = await session.execute(statement)
    gifts = result.scalars().all()
    return [GiftSchema.model_validate(gift) for gift in gifts]


async def get_gift_by_id(session: AsyncSession, gift_id: int) -> GiftSchema:
    statement = (
        select(Gift)
        .options(
            joinedload(Gift.brand).selectinload(GiftBrand.gifts),
            selectinload(Gift.ages).selectinload(BoardGameAge.board_game),
            joinedload(Gift.seria),
            selectinload(Gift.images),
            joinedload(Gift.gift_category),
            joinedload(Gift.gift_subcategory)
        )
        .where(Gift.id == gift_id)
    )

    result: Result = await session.execute(statement)
    gift = result.scalars().first()
    if not gift:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gift not found")
    return GiftSchema.model_validate(gift)


async def get_gift_by_slug(session: AsyncSession, gift_slug: str) -> GiftSchema:
    statement = (
        select(Gift)
        .options(
            joinedload(Gift.brand).selectinload(GiftBrand.gifts),
            selectinload(Gift.ages).selectinload(BoardGameAge.board_game),
            joinedload(Gift.seria),
            selectinload(Gift.images),
            joinedload(Gift.gift_category),
            joinedload(Gift.gift_subcategory)
        )
        .where(Gift.slug == gift_slug)
    )

    result: Result = await session.execute(statement)
    gift = result.scalars().first()
    if not gift:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gift not found")
    return GiftSchema.model_validate(gift)


async def update_gift(session: AsyncSession, gift_id: int, gift_data: GiftUpdate) -> GiftSchema:
    gift = await session.get(Gift, gift_id)

    if not gift:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gift not found")

    for key, value in gift_data.model_dump(exclude_unset=True).items():
        setattr(gift, key, value)

    try:
        await session.commit()
        await session.refresh(gift)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return GiftSchema.model_validate(gift)


async def delete_gift_by_id(session: AsyncSession, gift_id: int) -> bool:
    statement = delete(Gift).where(Gift.id == gift_id)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        await session.rollback()
        return False


async def main():
    async with db_helper.session_factory() as session:
        for gift in GIFTS:
            await create_gift(session, GiftCreate.model_validate(gift))


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())

