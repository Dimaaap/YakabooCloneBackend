import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from banners.views import SIX_DAYS
from notebook_categories.schema import NotebookCategorySchema, NotebookCategoryCreate
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["Notebook Categories"])

REDIS_KEY = "notebook_categories"


@router.get("/all", response_model=list[NotebookCategorySchema])
async def get_all_notebook_categories(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_categories = await redis_client.get(REDIS_KEY)

    if cached_categories:
        return json.loads(cached_categories)

    categories = await crud.get_all_notebook_categories(session)
    await redis_client.set(REDIS_KEY, json.dumps([category.model_dump() for category in categories]))
    return categories


@router.get("/{slug}", response_model=NotebookCategorySchema)
async def get_notebook_category_by_slug(slug: str,
                                        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_categories = await redis_client.get(REDIS_KEY)

    if cached_categories:
        categories_list = json.loads(cached_categories)

        for category in categories_list:
            if category["slug"] == slug:
                return category
    else:
        categories = await crud.get_all_notebook_categories(session)
        await redis_client.set(REDIS_KEY, json.dumps([category.model_dump() for category in categories]))
        return await crud.get_notebook_category_by_slug(session, slug)


@router.get("/{category_id}", response_model=NotebookCategorySchema)
async def get_notebook_category_by_id(category_id: int,
                                      session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_categories = await redis_client.get(REDIS_KEY)

    if cached_categories:
        categories_list = json.loads(cached_categories)
        for category in categories_list:
            if category["id"] == category_id:
                return category
    else:
        categories = await crud.get_notebook_category_by_id(session, category_id)
        await redis_client.set(REDIS_KEY,
                               json.dumps([category.model_dump() for category in categories]))
        return await crud.get_notebook_category_by_id(session, category_id)


@router.get("/books/{category_slug}")
async def get_books_by_category_slug(category_slug: str,
                                     session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    category = await crud.get_notebooks_by_category_slug(session, category_slug)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category


@router.post("/create")
async def create_notebook_category(
        notebook_category: NotebookCategoryCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    new_category = await crud.create_notebook_category(session, notebook_category)

    if new_category:
        await redis_client.delete(REDIS_KEY)
        return new_category

    return {"message": "Error while creating new notebook category"}


@router.delete("/{category_id}")
async def delete_notebook_category_by_id(
        category_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    deleted_category = crud.delete_notebook_category_by_id(session, category_id)

    if deleted_category:
        await redis_client.delete(REDIS_KEY)
        return {"message": f"The notebook category with id {category_id} was deleted"}
    return {"error": deleted_category}