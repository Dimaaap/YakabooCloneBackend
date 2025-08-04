import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import HobbyCategory, db_helper
from hobby_categories.schemas import HobbyCategorySchema, HobbyCategoryCreate

from data_strorage import HOBBY_CATEGORIES


async def create_hobby_category(
        session: AsyncSession,
        hobby_category: HobbyCategoryCreate
) -> HobbyCategorySchema:
    category = HobbyCategory(**hobby_category.model_dump())

    try:
        session.add(category)
        await session.commit()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return category


async def get_all_hobby_categories(session: AsyncSession) -> list[HobbyCategory]:
    statement = select(HobbyCategory).order_by(HobbyCategory.id)

    result: Result = await session.execute(statement)
    hobby_categories = result.scalars().all()
    return [HobbyCategorySchema.model_validate(category) for category in hobby_categories]


async def get_hobby_category_by_slug(session: AsyncSession, slug: str):
    statement = select(HobbyCategory).where(HobbyCategory.slug == slug)

    result: Result = await session.execute(statement)
    hobby_category = result.scalars().first()

    if not hobby_category:
        return []
    return hobby_category


async def get_hobby_category_by_id(session: AsyncSession, category_id: int) -> HobbyCategorySchema:
    statement = select(HobbyCategory).where(HobbyCategory.id == category_id)

    result: Result = await session.execute(statement)
    category = result.scalars().first()

    if not category:
        return []
    return category


async def delete_hobby_category_by_id(session: AsyncSession, category_id: int):
    statement = delete(HobbyCategory).where(HobbyCategory.id == category_id)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False


async def main():
    async with db_helper.session_factory() as session:
        for category in HOBBY_CATEGORIES:
            category = HobbyCategoryCreate(**category)
            await create_hobby_category(session, category)


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
