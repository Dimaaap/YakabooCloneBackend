import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import GiftCategory, db_helper, Gift, BoardGameAge
from gift_categories.schemas import GiftCategorySchema, GiftCategoryCreate

from data_strorage import GIFT_CATEGORIES


async def create_gift_category(
        session: AsyncSession,
        gift_category: GiftCategoryCreate
) -> GiftCategorySchema:
    category = GiftCategory(**gift_category.model_dump())

    try:
        session.add(category)
        await session.commit()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return category


async def get_all_gift_categories(session: AsyncSession) -> list[GiftCategorySchema]:
    statement = (
        select(GiftCategory)
        .options(selectinload(GiftCategory.subcategories))
        .order_by(GiftCategory.id)
    )

    result: Result = await session.execute(statement)
    hobby_categories = result.unique().scalars().all()
    return [GiftCategorySchema.model_validate(category) for category in hobby_categories]


async def get_gift_category_by_slug(session: AsyncSession, slug: str) -> GiftCategorySchema | None:
    statement = (
        select(GiftCategory)
        .where(GiftCategory.slug == slug)
        .options(
            selectinload(GiftCategory.subcategories)
        )
    )

    result: Result = await session.execute(statement)
    gift_category = result.unique().scalars().first()
    if not gift_category:
        return None
    return GiftCategorySchema.model_validate(gift_category)


async def get_gifts_by_category_slug(session: AsyncSession, category_slug: str):
    statement = (
        select(GiftCategory)
        .where(GiftCategory.slug == category_slug)
        .options(
            selectinload(GiftCategory.gifts)
            .joinedload(Gift.brand),
            selectinload(GiftCategory.gifts).selectinload(Gift.ages).selectinload(BoardGameAge.board_game),
            selectinload(GiftCategory.gifts).joinedload(Gift.seria),
            selectinload(GiftCategory.gifts).selectinload(Gift.images),
            selectinload(GiftCategory.subcategories)
        )
    )

    result: Result = await session.execute(statement)
    category = result.scalars().first()
    return category


async def get_gift_category_by_id(session: AsyncSession, category_id: int) -> GiftCategorySchema:
    statement = select(GiftCategory).where(GiftCategory.id == category_id)

    result: Result = await session.execute(statement)
    category = result.scalars().first()

    if not category:
        return []
    return category


async def delete_gift_category_by_id(session: AsyncSession, category_id: int):
    statement = delete(GiftCategory).where(GiftCategory.id == category_id)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False


async def main():
    async with db_helper.session_factory() as session:
        for category in GIFT_CATEGORIES:
            category = GiftCategoryCreate(**category)
            await create_gift_category(session, category)


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
