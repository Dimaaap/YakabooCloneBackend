from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.double_subcategories.schema import DoubleSubcategoriesForAdminList
from core.models import DoubleSubcategory


async def get_double_subcategories_for_admin_page(session: AsyncSession) -> list[DoubleSubcategoriesForAdminList]:
    statement = (
        select(DoubleSubcategory)
        .options(joinedload(DoubleSubcategory.subcategory))
        .order_by(DoubleSubcategory.id)
    )

    result = await session.execute(statement)
    double_subcategories = result.scalars().all()

    for subcategory in double_subcategories:
        subcategory.subcategory_title = subcategory.subcategory.title
        subcategory.images = [src["image_src"] for src in subcategory.images_src]

    return [
        DoubleSubcategoriesForAdminList.model_validate(subcategory)
        for subcategory in double_subcategories
    ]

async def get_double_subcategory_field_data(session: AsyncSession, double_subcategory_id: int) -> DoubleSubcategoriesForAdminList:
    statement = (
        select(DoubleSubcategory)
        .options(
            joinedload(DoubleSubcategory.subcategory)
        )
        .where(DoubleSubcategory.id == double_subcategory_id)
    )

    result = await session.execute(statement)
    double_subcategory = result.scalars().first()

    double_subcategory.subcategory_title = double_subcategory.subcategory.title
    double_subcategory.images = [src["image_src"] for src in double_subcategory.images_src]

    return DoubleSubcategoriesForAdminList.model_validate(double_subcategory)