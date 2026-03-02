from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.promo_categories.schema import PromoCategoriesForAdmin
from core.models import PromoCategories


async def get_promo_categories_for_admin_page(session: AsyncSession) -> list[PromoCategoriesForAdmin]:
    statement = (
        select(PromoCategories)
        .order_by(PromoCategories.id)
    )

    result = await session.execute(statement)
    promo_categories = result.scalars().all()

    return [
        PromoCategoriesForAdmin.model_validate(category)
        for category in promo_categories
    ]


async def get_promo_categories_field_data(session: AsyncSession, category_slug: str) -> PromoCategoriesForAdmin:
    statement = (
        select(PromoCategories)
        .where(PromoCategories.slug == category_slug)
    )

    result = await session.execute(statement)
    promo_category = result.scalars().first()

    return PromoCategoriesForAdmin.model_validate(promo_category)