import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Category, Subcategory, db_helper
from data_strorage import CATEGORIES, SUB_CATEGORIES
from categories.schemas import CategoryCreate, SubCategoryBase, CategorySchema, SubCategorySchema


async def create_category(session: AsyncSession, category: CategoryCreate) -> Category:
    category = Category(**category.model_dump())
    try:
        session.add(category)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return category


async def create_sub_category(session: AsyncSession, sub_category: SubCategoryBase) -> Subcategory:
    sub_category = Subcategory(**sub_category.model_dump())
    try:
        session.add(sub_category)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return sub_category


async def delete_category_by_id(session: AsyncSession, category_id: int):
    statement = delete(Category).where(Category.id == category_id)
    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        await session.rollback()
        return False


async def delete_subcategory_by_id(session: AsyncSession, subcategory_id: int):
    statement = delete(Subcategory).where(Subcategory.id == subcategory_id)
    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        await session.rollback()
        return False


async def get_all_subcategories(session: AsyncSession) -> list[SubCategorySchema]:
    statement = select(Subcategory).order_by(Subcategory.id)
    result: Result = await session.execute(statement)
    subcategories = result.scalars().all()
    return [SubCategorySchema.model_validate(subcategory) for subcategory in subcategories]


async def get_all_subcategories_by_category_id(session: AsyncSession, category_id: int) -> list[SubCategorySchema]:
    statement = select(Subcategory).where(Subcategory.category_id == category_id).order_by(Subcategory.title)
    try:
        result: Result = await session.execute(statement)
        subcategories = result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return [SubCategorySchema.model_validate(subcategory) for subcategory in subcategories]


async def get_all_categories(session: AsyncSession) -> list[CategorySchema]:
    statement = select(Category).order_by(Category.id)
    result: Result = await session.execute(statement)
    categories = result.scalars().all()
    return [CategorySchema.model_validate(category) for category in categories]


async def main():
    async with db_helper.session_factory() as session:
        for category in CATEGORIES:
            await create_category(session, CategoryCreate.model_validate(category))

        for sub_category in SUB_CATEGORIES:
            await create_sub_category(session, SubCategoryBase.model_validate(sub_category))


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())