from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.promotions.schema import PromotionsForAdminPage, EditPromotion
from core.models import Promotion, PromoCategories


async def get_promotions_for_admin_page(session: AsyncSession) -> list[PromotionsForAdminPage]:
    statement = (
        select(Promotion)
        .options(selectinload(Promotion.categories))
        .order_by(Promotion.id)
    )

    result = await session.execute(statement)
    promotions = result.scalars().all()

    for promotion in promotions:
        promotion.categories_title = [category.title for category in promotion.categories]

    return [
        PromotionsForAdminPage.model_validate(promotion)
        for promotion in promotions
    ]


async def get_all_categories(session: AsyncSession) -> list[PromoCategories]:
    statement = select(PromoCategories).order_by(PromoCategories.title)
    result = await session.execute(statement)
    return result.scalars().all()


async def get_promotion_field_data(session: AsyncSession, promotion_id: int) -> PromotionsForAdminPage:
    statement = (
        select(Promotion)
        .options(selectinload(Promotion.categories))
        .where(Promotion.id == promotion_id)
    )

    result = await session.execute(statement)
    promotion = result.scalars().first()

    promotion.categories_title = [category.title for category in promotion.categories]

    return PromotionsForAdminPage.model_validate(promotion)


async def get_promotion_by_id(session: AsyncSession, promo_id: int) -> Promotion | bool:
    promo = await session.get(Promotion, promo_id)

    if not promo:
        return False

    return promo


async def update_promotion(session: AsyncSession, promo_id: int, data: EditPromotion) -> bool:
    promo = await get_promotion_by_id(session, promo_id)

    if not promo:
        raise NotFoundInDbError("Promotion not found")

    update_data = data.model_dump(exclude_uset=True)

    for field, value in update_data.items():
        setattr(promo, field, value)

    await session.commit()

    return True