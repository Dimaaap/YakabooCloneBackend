import asyncio

from sqlalchemy import select, Result, delete, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import GiftBrand, db_helper, Gift, BoardGameAge
from gift_brands.schemas import GiftBrandSchema, GiftBrandCreate


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