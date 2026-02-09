import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession

from data_strorage import PROMO_CATEGORIES
from entities.promotion_categories.schemas import PromoCategoryCreate
from core.models import db_helper, PromoCategories


async def create_promotion_category(
        session: AsyncSession,
        promo_category: PromoCategoryCreate
) -> PromoCategories:
    promo_category = PromoCategories(**promo_category.model_dump())
    try:
        session.add(promo_category)
        await session.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    return promo_category


async def delete_promo_category(
        session: AsyncSession,
        category_id: int
):
    statement = delete(PromoCategories).where(PromoCategories.id == category_id)
    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        await session.rollback()
        return False


async def get_all_promotion_categories(session: AsyncSession) -> list[PromoCategories]:
    statement = select(PromoCategories).order_by(PromoCategories.id).where(PromoCategories.is_active)
    result: Result = await session.execute(statement)
    promo_categories = result.scalars().all()
    return list(promo_categories)


async def main():
    async with db_helper.session_factory() as session:
        for promo_category in PROMO_CATEGORIES:
            await create_promotion_category(session, PromoCategoryCreate.model_validate(promo_category))


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())