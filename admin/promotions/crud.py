from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.promo_categories.crud import get_promo_categories_for_admin_page
from admin.promotions.schema import PromotionsForAdminPage, EditPromotion, CreatePromotion
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

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(promo, field, value)

    await session.commit()
    await session.refresh(promo)
    return True


async def create_promotion(session: AsyncSession, data: CreatePromotion) -> Promotion | bool:
    promotion = Promotion(
        title=data.title,
        slug=data.slug,
        image=data.image,
        main_description=data.main_description,
        short_description=data.short_description,
        long_description=data.long_description,
        end_date=data.end_date,
        is_active=data.is_active,
    )

    session.add(promotion)
    if data.categories is not None:
        result = await session.execute(
            select(PromoCategories).where(PromoCategories.slug.in_(data.categories))
        )

        result = result.scalars().unique().all()
        promotion.categories = result
    else:
        promotion.categories = []
    try:
        await session.commit()
        await session.refresh(promotion)
    except SQLAlchemyError:
        await session.rollback()
        return False
    return promotion


async def set_promotion_categories_in_choices(session: AsyncSession, form):
    categories = await get_promo_categories_for_admin_page(session)
    choices = [(cat.slug, cat.title) for cat in categories]
    form.categories.choices = choices