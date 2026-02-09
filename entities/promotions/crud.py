import asyncio
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from entities.promotions.schemas import PromotionCreate
from core.models import Promotion, db_helper, PromoCategoryAssociation, PromoCategories
from data_strorage import PROMOS


async def create_promotion(
        session: AsyncSession,
        promo: PromotionCreate
) -> Promotion:
    promotion = Promotion(**promo.model_dump(exclude={"category_ids"}))
    session.add(promotion)
    await session.flush()

    for category_id in promo.category_ids:
        association = PromoCategoryAssociation(
            category_id=category_id,
            promotion_id=promotion.id
        )
        session.add(association)
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return promotion


async def get_all_promotions(session: AsyncSession) -> list[Promotion]:
    statement = select(Promotion).order_by(Promotion.id).where(
        Promotion.is_active,
        (Promotion.end_date.is_(None) | (Promotion.end_date > datetime.now()))
    )
    result: Result = await session.execute(statement)
    promotions = result.scalars().all()
    return list(promotions)


async def get_promotions_by_slug(promotion_slug: str,
                                 session: AsyncSession) -> Promotion:
    statement = select(Promotion).where(Promotion.slug == promotion_slug)
    result: Result = await session.execute(statement)
    promotion = result.scalars().first()
    if not promotion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
    return promotion


async def get_promotion_by_id(promotion_id: int,
                              session: AsyncSession) -> Promotion:
    statement = select(Promotion).where(Promotion.id == promotion_id)
    result: Result = await session.execute(statement)
    promotion = result.scalars().first()
    if not promotion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
    return promotion


async def get_all_promotions_by_category_id(
        session: AsyncSession, category_id: int
) -> list[Promotion]:
    statement = (
        select(Promotion)
        .join(PromoCategoryAssociation, PromoCategoryAssociation.promotion_id == Promotion.id)
        .filter(PromoCategoryAssociation.category_id == category_id))
    result: Result = await session.execute(statement)
    promotions = result.scalars().all()
    return list(promotions)


async def get_all_promotions_by_category_slug(session: AsyncSession, category_slug: str) -> list[Promotion]:
    statement = select(Promotion).join(
        PromoCategoryAssociation,
        PromoCategoryAssociation.promotion_id == Promotion.id
    ).join(PromoCategories, PromoCategories.id == PromoCategoryAssociation.category_id).filter(
        PromoCategories.slug == category_slug,
        (Promotion.end_date.is_(None) | (Promotion.end_date > datetime.now()))
    )
    result: Result = await session.execute(statement)
    promotions = result.scalars().all()
    return list(promotions)


async def get_all_promotions_with_categories(session: AsyncSession) -> list[PromoCategories]:
    statement = select(PromoCategories).options(selectinload(PromoCategories.promotions)).order_by(PromoCategories.id)
    result: Result = await session.execute(statement)
    promo_categories = result.scalars().all()
    return list(promo_categories)


async def delete_promotion_by_id(promotion_id: int,
                                 session: AsyncSession) -> bool | None:
    statement = delete(Promotion).where(Promotion.id == promotion_id)
    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e))


async def main():
    async with db_helper.session_factory() as session:
        for promo in PROMOS:
            await create_promotion(session=session, promo=PromotionCreate.model_validate(promo))


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())