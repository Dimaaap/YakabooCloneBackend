import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import HobbySubCategory, db_helper, HobbyCategory, Hobby, BoardGameAge
from data_strorage import HOBBY_SUBCATEGORIES
from hobby_subcategories.schema import HobbySubcategorySchema, HobbySubcategoryCreate


async def create_hobby_subcategory(
        session: AsyncSession,
        hobby_subcategory: HobbySubcategoryCreate,
) -> HobbySubcategorySchema:
    subcategory = HobbySubCategory(**hobby_subcategory.model_dump())

    try:
        session.add(subcategory)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return subcategory



async def get_all_hobby_subcategories(session: AsyncSession) -> list[HobbySubCategory]:
    statement = select(HobbySubCategory).order_by(HobbySubCategory.id)

    result: Result = await session.execute(statement)
    hobby_subcategories = result.scalars().all()
    return [HobbySubcategorySchema.model_validate(subcategory) for subcategory in hobby_subcategories]


async def get_hobby_subcategory_by_slug(session: AsyncSession, slug: str):
    statement = select(HobbySubCategory).where(HobbySubCategory.slug == slug)

    result: Result = await session.execute(statement)
    hobby_subcategory = result.scalars().first()

    if not hobby_subcategory:
        return []

    return hobby_subcategory


async def get_hobbies_by_subcategory_slug(session: AsyncSession, subcategory_slug: str):
    statement = (
        select(HobbySubCategory)
        .where(HobbySubCategory.slug == subcategory_slug)
        .options(
            selectinload(HobbySubCategory.hobbies)
            .joinedload(Hobby.brand),
            selectinload(HobbySubCategory.hobbies).selectinload(Hobby.ages).selectinload(BoardGameAge.board_game),
            selectinload(HobbySubCategory.hobbies).joinedload(Hobby.seria),
            selectinload(HobbyCategory.hobbies).selectinload(Hobby.images)
        )
    )

    result: Result = await session.execute(statement)
    subcategory = result.scalars().first()
    return subcategory


async def get_hobby_subcategory_by_id(session: AsyncSession, subcategory_id: int) -> HobbySubcategorySchema:
    statement = select(HobbySubCategory).where(HobbySubCategory.id == subcategory_id)

    result: Result = await session.execute(statement)
    subcategory = result.scalars().first()

    if not subcategory:
        return []
    return subcategory


async def delete_hobby_subcategory_by_id(session: AsyncSession, subcategory_id: int):
    statement = delete(HobbySubCategory).where(HobbySubCategory.id == subcategory_id)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False


async def main():
    async with db_helper.session_factory() as session:
        for subcategory in HOBBY_SUBCATEGORIES:
            await create_hobby_subcategory(session, HobbySubcategoryCreate.model_validate(subcategory))


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

