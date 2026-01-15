import asyncio
from typing import Iterable

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from books.crud import BASE_FILTER, BOOK_OPTIONS
from books.services import BookFilter
from core.models import Category, Subcategory, db_helper, Book, Author
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
    statement = (select(Category).options(selectinload(Category.banners),
                                          selectinload(Category.subcategories),
                                          selectinload(Category.books))
                 .order_by(Category.id))
    result: Result = await session.execute(statement)
    categories = result.scalars().all()
    return [CategorySchema.model_validate(category) for category in categories]


async def get_category_by_id(session: AsyncSession, category_id: int) -> CategorySchema:
    statement = (select(Category)
                 .options(selectinload(Category.banners), selectinload(Category.subcategories))
                 .where(Category.id == category_id)
                 )
    result: Result = await session.execute(statement)
    category = result.unique().scalars().first()
    return category


async def get_all_category_books_by_category_slug(session: AsyncSession, category_slug: str,
                                                  limit: int, offset: int, filter) -> tuple[list, int]:
    base_query = (select(Book)
                  .join(Book.categories)
                  .where(BASE_FILTER, Category.slug == category_slug))
    bf = BookFilter(filter)
    conditions = bf.apply()

    if conditions:
        base_query = base_query.where(and_(*conditions))

    total_statement = select(func.count()).select_from(base_query.subquery())
    total = await session.scalar(total_statement)

    statement = (
        base_query
        .options(*BOOK_OPTIONS)
        .offset(offset)
        .limit(limit)
    )

    result: Result = await session.execute(statement)
    books = result.unique().scalars().all()
    if not books:
        return [], 0
    return books, total


async def get_all_books_by_category_id(session: AsyncSession, category_id: int):
    statement = (
        select(Book)
        .join(Book.categories)
        .where(Category.id == category_id)
        .options(
            selectinload(Book.authors).joinedload(Author.interesting_fact),
            selectinload(Book.authors).selectinload(Author.images),
            selectinload(Book.translators),
            selectinload(Book.illustrators),
            selectinload(Book.images),
            joinedload(Book.book_info),
            joinedload(Book.publishing),
            joinedload(Book.literature_period),
            joinedload(Book.seria),
            joinedload(Book.edition_group),
        )
    )

    result: Result = await session.execute(statement)
    books = result.unique().scalars().all()
    if not books:
        return []
    return books


async def get_category_by_slug(session: AsyncSession, category_slug: str) -> CategorySchema:
    statement = (select(Category).options(
        selectinload(Category.banners),
        selectinload(Category.subcategories)
    )
    .where(Category.slug == category_slug))

    result: Result = await session.execute(statement)
    category = result.scalars().first()
    return category


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