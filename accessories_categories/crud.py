import asyncio

from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import AccessoriesCategory, db_helper, BookAccessories
from accessories_categories.schemas import AccessoryCategorySchema, AccessoryCategoryCreate
from data_strorage import ACCESSORIES_CATEGORIES


async def create_accessory_category(
        session: AsyncSession,
        category: AccessoryCategoryCreate
) -> AccessoriesCategory:
    new_category = AccessoriesCategory(**category.model_dump())

    if category.accessories:
        statement = select(BookAccessories).where(BookAccessories.id.in_(category.accessories))
        result: Result = await session.execute(statement)
        accessories = result.scalars().all()

        for accessory in accessories:
            accessory.category = new_category

    session.add(new_category)
    await session.commit()
    await session.refresh(new_category)
    return new_category


async def delete_category_by_id(session: AsyncSession, category_id: int):
    statement = delete(AccessoriesCategory).where(AccessoriesCategory.id == category_id)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False


async def get_category_by_slug(session: AsyncSession, category_slug: str) -> AccessoriesCategory:
    statement = (select(AccessoriesCategory)
                 .options(selectinload(AccessoriesCategory.accessories))
                 .where(AccessoriesCategory.slug == category_slug))
    result: Result = await session.execute(statement)
    category = result.scalars().first()
    return category


async def get_all_accessories_by_category_slug(session: AsyncSession, category_slug: str):
    statement = (
        select(AccessoriesCategory)
        .where(AccessoriesCategory.slug == category_slug)
        .options(
            selectinload(AccessoriesCategory.accessories),
            selectinload(AccessoriesCategory.accessories).selectinload(BookAccessories.images)
        )
    )

    result: Result = await session.execute(statement)
    category = result.scalars().all()
    return category


async def get_all_categories(session) -> list[AccessoryCategorySchema]:
    statement = (
        select(AccessoriesCategory)
        .options(selectinload(AccessoriesCategory.accessories))
        .order_by(AccessoriesCategory.title)
    )

    result: Result = await session.execute(statement)
    categories = result.scalars().all()
    return categories


async def main():
    async with db_helper.session_factory() as session:
        for category in ACCESSORIES_CATEGORIES:
            category = AccessoryCategoryCreate(**category)
            await create_accessory_category(session, category)


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())