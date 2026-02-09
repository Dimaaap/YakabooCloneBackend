import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import NotebookSubcategorySchema, NotebookSubcategoryCreate
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["Notebook Subcategories"])
REDIS_KEY = "notebook_subcategories"


@router.get("/all", response_model=list[NotebookSubcategorySchema])
async def get_all_notebook_subcategories(session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    cached_subcategories = await redis_client.get(REDIS_KEY)

    if cached_subcategories:
        return json.loads(cached_subcategories)

    subcategories = await crud.get_all_notebook_subcategories(session)
    await redis_client.set(REDIS_KEY, json.dumps([sub.model_dump() for sub in subcategories]))
    return subcategories


@router.get("/{slug}", response_model=NotebookSubcategorySchema)
async def get_notebook_subcategory_by_slug(slug: str,
                                           session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    cached_subcategories = await redis_client.get(REDIS_KEY)

    if cached_subcategories:
        sub_list = json.loads(cached_subcategories)

        for sub in sub_list:
            if sub["slug"] == slug:
                return sub
    else:
        subcategories = await crud.get_all_notebook_subcategories(session)
        await redis_client.set(REDIS_KEY, json.dumps([sub.model_dump() for sub in subcategories]))
        return await crud.get_notebook_subcategory_by_slug(session, slug)


@router.get("/notebooks/{slug}")
async def get_notebooks_by_subcategory_slug(slug: str,
                                            session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    subcategory = await crud.get_notebooks_by_subcategory_slug(session, slug)
    return subcategory


@router.get("/by-id/{subcategory_id}", response_model=NotebookSubcategorySchema)
async def get_notebook_subcategory_by_id(subcategory_id: int,
                                         session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    cached_subcategories = await redis_client.get(REDIS_KEY)

    if cached_subcategories:
        sub_list = json.loads(cached_subcategories)
        for sub in sub_list:
            if sub["id"] == subcategory_id:
                return sub

    else:
        sub_list = await crud.get_all_notebook_subcategories(session)
        await redis_client.set(REDIS_KEY, json.dumps([sub.model_dump() for sub in sub_list]))
        return await crud.get_notebook_subcategory_by_id(session, subcategory_id)


@router.post("/create")
async def create_notebook_subcategory(notebook_subcategory: NotebookSubcategoryCreate,
                                      session: AsyncSession=Depends(db_helper.scoped_session_dependency)):

    new_subcategory = await crud.create_notebook_subcategory(session, notebook_subcategory)

    if new_subcategory:
        await redis_client.delete(REDIS_KEY)
        return new_subcategory

    return {"message": "Error while create new notebook subcategory"}


@router.delete("/{subcategory_id}")
async def delete_notebook_subcategory_by_id(subcategory_id: int,
                                            session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    deleted_subcategory = await crud.delete_notebook_subcategory_by_id(session, subcategory_id)

    if deleted_subcategory:
        await redis_client.delete(REDIS_KEY)
        return {"message": f"The hobby subcategory { subcategory_id } was deleted"}

    return {"error": deleted_subcategory}