import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import NotebookSubCategory, db_helper, Book, Hobby, Author
from data_strorage import NOTEBOOK_SUBCATEGORIES
from notebook_subcategories.schemas import NotebookSubcategorySchema, NotebookSubcategoryCreate


async def create_notebook_subcategory(
        session: AsyncSession,
        notebook_subcategory: NotebookSubcategoryCreate,
) -> NotebookSubcategorySchema:
    subcategory = NotebookSubCategory(**notebook_subcategory.model_dump())

    try:
        session.add(subcategory)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return subcategory


async def get_all_notebook_subcategories(session: AsyncSession) -> list[NotebookSubcategorySchema]:
    statement = select(NotebookSubCategory).order_by(NotebookSubCategory.id)

    result: Result = await session.execute(statement)
    notebook_subcategories = result.scalars().all()
    return [NotebookSubcategorySchema.model_validate(subcategory) for subcategory in notebook_subcategories]


async def get_notebook_subcategory_by_slug(session: AsyncSession, slug: str):
    statement = select(NotebookSubCategory).where(NotebookSubCategory.slug == slug)

    result: Result = await session.execute(statement)
    notebook_subcategory = result.scalars().first()

    if not notebook_subcategory:
        return []

    return notebook_subcategory


async def get_notebooks_by_subcategory_slug(session: AsyncSession, subcategory_slug: str):
    statement = (
        select(NotebookSubCategory)
        .where(NotebookSubCategory.slug == subcategory_slug)
        .options(
            selectinload(NotebookSubCategory.notebooks).joinedload(Book.book_info),
            selectinload(NotebookSubCategory.notebooks).joinedload(Book.publishing),
            selectinload(NotebookSubCategory.notebooks).selectinload(Book.authors).selectinload(Author.interesting_fact),
            selectinload(NotebookSubCategory.notebooks).selectinload(Book.authors).selectinload(Author.images),
            selectinload(NotebookSubCategory.notebooks).selectinload(Book.images),
            selectinload(NotebookSubCategory.notebooks).selectinload(Book.translators),
            selectinload(NotebookSubCategory.notebooks).joinedload(Book.literature_period),
        )
    )

    result: Result = await session.execute(statement)
    subcategory = result.scalars().first()
    return subcategory


async def get_notebook_subcategory_by_id(session: AsyncSession, subcategory_id: int):
    statement = select(NotebookSubCategory).where(NotebookSubCategory.id == subcategory_id)

    result: Result = await session.execute(statement)
    subcategory = result.scalars().first()

    if not subcategory:
        return []
    return subcategory


async def delete_notebook_subcategory_by_id(session: AsyncSession, subcategory_id: int):
    statement = delete(NotebookSubCategory).where(NotebookSubCategory.id == subcategory_id)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False

async def main():
    async with db_helper.session_factory() as session:
        for subcategory in NOTEBOOK_SUBCATEGORIES:
            await create_notebook_subcategory(session, NotebookSubcategoryCreate.model_validate(subcategory))


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())



