from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.subcategories.schema import SubCategoriesForAdminList, EditSubCategory
from core.models import Subcategory


async def get_subcategories_for_admin_page(session: AsyncSession) -> list[SubCategoriesForAdminList]:
    statement = (
        select(Subcategory)
        .options(joinedload(Subcategory.category))
        .order_by(Subcategory.id)
    )

    result = await session.execute(statement)
    subcategories = result.scalars().all()

    for sub in subcategories:
        sub.category_title = sub.category.title
        sub.images = [src["image_src"] for src in sub.images_src] if sub.images_src else []

    return [
        SubCategoriesForAdminList.model_validate(sub)
        for sub in subcategories
    ]


async def get_subcategory_field_data(session: AsyncSession, subcategory_id: int) -> SubCategoriesForAdminList:
    statement = (
        select(Subcategory)
        .options(
            joinedload(Subcategory.category)
        )
        .where(Subcategory.id == subcategory_id)
    )

    result = await session.execute(statement)
    subcategory = result.scalars().first()

    subcategory.category_title = subcategory.category.title
    subcategory.images = [src["image_src"] for src in subcategory.images_src] if subcategory.images_src else []

    return SubCategoriesForAdminList.model_validate(subcategory)


async def get_subcategory_by_id(session: AsyncSession, subcategory_id: int) -> Subcategory | bool:
    subcategory = await session.get(Subcategory, subcategory_id)

    if not subcategory:
        return False

    return subcategory


async def update_subcategory(session: AsyncSession, subcategory_id: int,
                             data: EditSubCategory) -> bool:
    subcategory = await get_subcategory_by_id(session, subcategory_id)

    if not subcategory:
        raise NotFoundInDbError("Subcategory not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(subcategory, field, value)

    await session.commit()
    await session.refresh(subcategory)
    return True
