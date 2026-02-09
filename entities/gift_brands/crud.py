import asyncio

from sqlalchemy import select, Result, delete, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import GiftBrand, db_helper, Gift, BoardGameAge
from data_strorage import GIFT_BRANDS
from entities.gift_brands.schemas import GiftBrandSchema, GiftBrandCreate


async def create_gift_brand(
        session: AsyncSession,
        brand: GiftBrandCreate
) -> GiftBrand:
    new_brand = GiftBrand(**brand.model_dump())

    if brand.gifts:
        statement = select(Gift).where(Gift.id.in_(brand.hobbies))
        result = await session.execute(statement)
        gifts = result.scalars().all()

        for gift in gifts:
            gift.brand = new_brand
    session.add(new_brand)
    await session.commit()
    await session.refresh(new_brand)
    return new_brand


async def delete_brand_by_id(session: AsyncSession, brand_id: int) -> bool:
    statement = delete(GiftBrand).where(GiftBrand.id == brand_id)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False


async def get_brand_by_slug(session: AsyncSession, brand_slug: str) -> GiftBrand:
    statement = (select(GiftBrand)
                 .options(selectinload(GiftBrand.gifts))
                 .where(GiftBrand.slug == brand_slug, GiftBrand.visible)
                 )
    result: Result = await session.execute(statement)
    gift = result.scalars().first()
    return gift


async def get_brand_by_id(session: AsyncSession, brand_id: int) -> GiftBrand:
    statement = (select(GiftBrand)
                 .options(selectinload(GiftBrand.gifts))
                 .where(GiftBrand.id == brand_id, GiftBrand.visible))
    result: Result = await session.execute(statement)
    brand = result.scalars().first()
    return brand


async def get_brand_by_query(query: str, session: AsyncSession):
    query = query.strip()
    similarity = func.similarity(GiftBrand.title, query)

    statement = (
        select(GiftBrand)
        .where(
            GiftBrand.visible,
            or_(
                similarity >= 0.1,
                GiftBrand.title.like(f"%{query}%")
            )
        )
        .order_by(similarity)
    )

    result: Result = await session.execute(statement)
    gift_brands = result.scalars().all()
    return list(gift_brands) or []


async def get_all_gifts_by_brand_slug(brand_slug: str, session: AsyncSession):
    statement = (
        select(GiftBrand)
        .where(GiftBrand.slug == brand_slug, GiftBrand.visible)
        .options(
            selectinload(GiftBrand.gifts),
            selectinload(GiftBrand.gifts).selectinload(Gift.ages).selectinload(BoardGameAge.board_game),
            selectinload(GiftBrand.gifts).joinedload(Gift.seria),
            selectinload(GiftBrand.gifts).selectinload(Gift.images)
        )
    )

    result: Result = await session.execute(statement)
    brand = result.scalars().first()
    return brand


async def get_all_brands(session: AsyncSession) -> list[GiftBrandSchema]:
    statement = (select(GiftBrand)
                 .options(selectinload(GiftBrand.gifts))
                 .where(GiftBrand.visible)
                 .order_by(GiftBrand.id)
                 )
    result: Result = await session.execute(statement)
    brands = result.scalars().all()
    return [GiftBrandSchema.model_validate(brand) for brand in brands]

async def main():
    async with db_helper.session_factory() as session:
        for brand in GIFT_BRANDS:
            brand = GiftBrandCreate(**brand)
            await create_gift_brand(session, brand)


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())