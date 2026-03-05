from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.category.schema import CategoryForAdminList, EditCategory
from core.models import Category


async def get_categories_for_admin_page(session: AsyncSession) -> list[CategoryForAdminList]:
    statement = (
        select(Category)
        .options(
            selectinload(Category.banners),
            selectinload(Category.subcategories)
        )
        .order_by(Category.id)
    )

    result = await session.execute(statement)
    categories = result.scalars().all()

    for category in categories:
        category.subcategories_titles = [sub.title for sub in category.subcategories]
        category.banner_images = [banner.image_url for banner in category.banners]

    return [
        CategoryForAdminList.model_validate(category)
        for category in categories
    ]


async def get_category_field_data(session: AsyncSession, category_id: int) -> CategoryForAdminList:
    statement = (
        select(Category)
        .options(
            selectinload(Category.banners),
            selectinload(Category.subcategories)
        )
        .where(Category.id == category_id)
    )

    result = await session.execute(statement)
    category = result.scalars().first()

    category.subcategories_titles = [sub.title for sub in category.subcategories]
    category.banner_images = [banner.image_url for banner in category.banners]
    return CategoryForAdminList.model_validate(category)


async def get_book_category_by_id(session: AsyncSession, category_id: int) -> Category | bool:
    category = await session.get(Category, category_id)

    if not category:
        return False

    return category


async def update_book_category(session: AsyncSession, category_id: int, data: EditCategory) -> bool:
    category = await get_book_category_by_id(session, category_id)

    if not category:
        raise NotFoundInDbError("Book Category not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(category, field, value)

    await session.commit()

    return True