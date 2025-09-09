import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import NotebookCategory, db_helper, Book
from notebook_categories.schema import NotebookCategorySchema, NotebookCategoryCreate

from data_strorage import NOTEBOOK_CATEGORIES


async def create_notebook_category(
        session: AsyncSession,
        notebook_category: NotebookCategoryCreate
) -> NotebookCategorySchema:
    category = NotebookCategory(**notebook_category.model_dump())

    try:
        session.add(category)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return category


async def get_all_notebook_categories(session: AsyncSession) -> list[NotebookCategorySchema]:
    statement = select(NotebookCategory).order_by(NotebookCategory.id)

    result: Result = await session.execute(statement)
    notebook_categories = result.unique().scalars().all()
    return [NotebookCategorySchema.model_validate(category) for category in notebook_categories]


async def get_notebook_category_by_slug(session: AsyncSession, slug: str) -> NotebookCategorySchema | None:
    statement = select(NotebookCategory).where(NotebookCategory.slug == slug)

    result: Result = await session.execute(statement)
    notebook_category = result.unqiue().scalars().first()

    if not notebook_category:
        return None

    return NotebookCategorySchema.model_validate(notebook_category)


async def get_notebooks_by_category_slug(session: AsyncSession, category_slug: str):
    statement = (
        select(NotebookCategory)
        .where(NotebookCategory.slug == category_slug)
        .options(
            selectinload(NotebookCategory.notebooks).joinedload(Book.book_info),
            selectinload(NotebookCategory.notebooks).selectinload(Book.subcategories),
            selectinload(NotebookCategory.notebooks).joinedload(Book.literature_period),
            selectinload(NotebookCategory.notebooks).selectinload(Book.authors),
            selectinload(NotebookCategory.notebooks).selectinload(Book.images),
            selectinload(NotebookCategory.subcategories)
        )
    )

    result: Result = await session.execute(statement)
    category = result.unique().scalars().first()

    return category


async def get_notebook_category_by_id(session: AsyncSession, category_id: int) -> NotebookCategorySchema | None:
    statement = select(NotebookCategory).where(NotebookCategory.id == category_id)
    result: Result = await session.execute(statement)
    notebook_category = result.scalars().first()

    if not notebook_category:
        return None
    return NotebookCategorySchema.model_validate(notebook_category)


async def delete_notebook_category_by_id(session: AsyncSession, category_id: int) -> bool:
    statement = delete(NotebookCategory).where(NotebookCategory.id == category_id)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False


async def main():
    async with db_helper.session_factory() as session:
        for category in NOTEBOOK_CATEGORIES:
            category = NotebookCategoryCreate(**category)
            await create_notebook_category(session, category)


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())



