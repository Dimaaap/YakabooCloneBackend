import json

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CategorySchema, SubCategorySchema, CategoryCreate, SubCategoryBase
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["categories"])
SIX_DAYS = 24 * 3600 * 6


@router.get("/all", response_model=list[CategorySchema])
async def get_all_categories(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    cached_categories = await redis_client.get("categories")
    if cached_categories:
        return json.loads(cached_categories)

    categories = await crud.get_all_categories(session)
    await redis_client.set("categories",
                           json.dumps([category.model_dump() for category in categories]),
                           ex=SIX_DAYS)
    return categories


@router.get("/{category_id}")
async def get_category_by_id(category_id: int,
                             session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_categories = await redis_client.get("categories")

    if cached_categories:
        categories = json.loads(cached_categories)

        for category in categories:
            if category["id"] == category_id:
                return category
    else:
        categories = await crud.get_all_categories(session)
        await redis_client.set("categories",
                               json.dumps([category.model_dump() for category in categories]),
                               ex=SIX_DAYS)
        return await crud.get_category_by_id(session, category_id)



@router.post("/create", response_model=CategorySchema)
async def create_category(
        category: CategoryCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    new_category = await crud.create_category(session, category)
    if new_category:
        await redis_client.delete("categories")
        return new_category


@router.post("/subcategory/create", response_model=SubCategorySchema)
async def create_subcategory(
        subcategory: SubCategoryBase,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    new_subcategory = await crud.create_sub_category(session, subcategory)
    if new_subcategory:
        await redis_client.delete("subcategories")
        return new_subcategory


@router.delete("/{category_id}")
async def delete_category(
        category_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    deleted = await crud.delete_category_by_id(session, category_id)
    if deleted:
        await redis_client.delete("categories")
        await redis_client.delete(f"category_{category_id}_subcategories")
        return {"message": f"Category with id {category_id} has been deleted"}
    return {"message": "Server error while deleting"}


@router.delete("/subcategory/{subcategory_id}")
async def delete_subcategory(
        subcategory_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    deleted = await crud.delete_subcategory_by_id(session, subcategory_id)
    if deleted:
        await redis_client.delete("subcategories")
        return {"message": f"Subcategory with id {subcategory_id} has been deleted"}
    return {"message": "Server error while deleting"}


@router.get("/subcategories", response_model=list[SubCategorySchema])
async def get_all_subcategories(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    cached_subcategories = await redis_client.get("subcategories")
    if cached_subcategories:
        return json.loads(cached_subcategories)

    subcategories = await crud.get_all_subcategories(session)
    await redis_client.set("subcategories", json.dumps([subcategory.model_dump() for subcategory in subcategories]))
    return subcategories


@router.get("/{category_id}/subcategories", response_model=list[SubCategorySchema])
async def get_all_subcategories_by_category(
        category_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    cached_subcategories_by_category = await redis_client.get(f"category_{category_id}_subcategories")
    if cached_subcategories_by_category:
        return json.loads(cached_subcategories_by_category)

    subcategories_by_category = await crud.get_all_subcategories_by_category_id(session, category_id=category_id)
    await redis_client.set(f"category_{category_id}_subcategories",
                           json.dumps([subcategory.model_dump() for subcategory in subcategories_by_category]))
    return subcategories_by_category

