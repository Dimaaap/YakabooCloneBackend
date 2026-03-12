from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.promo_categories.schema import PromoCategoriesForAdmin, EditPromoCategory
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


async def get_promo_category_by_slug(session: AsyncSession, category_slug: str) -> PromoCategories | bool:
    statement = select(PromoCategories).where(PromoCategories.slug == category_slug)
    category_res = await session.execute(statement)
    category = category_res.scalar_one_or_none()

    if not category:
        return False

    return category


async def update_promo_category(session: AsyncSession, category_slug: str, data: EditPromoCategory) -> bool:
    promo_category = await get_promo_category_by_slug(session, category_slug)

    if not promo_category:
        raise NotFoundInDbError("Promo Category not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(promo_category, field, value)

    await session.commit()
    await session.refresh(promo_category)
    return True