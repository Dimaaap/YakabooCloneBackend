from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.promotions.schema import PromotionsForAdminPage
from core.models import Promotion


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