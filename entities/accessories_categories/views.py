import json

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import AccessoryCategorySchema, AccessoryCategoryCreate
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["Accessory Categories"])
REDIS_KEY = "accessories_categories"
SIX_DAYS = 24 * 3600 * 6

@router.get("/all", response_model=list[AccessoryCategorySchema])
async def get_all_categories(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_categories = await redis_client.get(REDIS_KEY)
    if cached_categories:
        return json.loads(cached_categories)

    categories = await crud.get_all_categories(session)
    await redis_client.set(REDIS_KEY, json.dumps([category.model_dump() for category in categories]),
                           ex=SIX_DAYS)
    return categories


@router.post("/create")
async def create_category(
        category: AccessoryCategoryCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    new_category = await crud.create_accessory_category(session, category)
    if not new_category:
        return {"message": "Error creating accessory category"}

    cached_categories = await redis_client.get(REDIS_KEY)
    if cached_categories:
        categories = json.loads(cached_categories)
        categories.append({
            "id": new_category.id,
            "title": new_category.title,
            "slug": new_category.slug,
            "images_src": new_category.images_src
        })
        await redis_client.set(REDIS_KEY, json.dumps(categories))
    return new_category



@router.delete("/{accessory_category_id}")
async def delete_category(
        accessory_category_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    cached_categories = await redis_client.get(REDIS_KEY)

    if cached_categories:
        categories = json.loads(cached_categories)
        updated_categories = [category for category in categories if category["id"] != accessory_category_id]
        await redis_client.set(REDIS_KEY, json.dumps(updated_categories), ex=SIX_DAYS)
    category = await crud.delete_category_by_id(session, accessory_category_id)

    if category:
        return {"message": f"Accesory category {accessory_category_id} deleted"}
    return {"error": category}


@router.get('/accessories/{category_slug}')
async def get_accessories_by_category(
        category_slug: str,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    category = await crud.get_all_accessories_by_category_slug(session, category_slug)

    return category or []


@router.get("/by-slug/{category_slug}")
async def get_category_by_slug(category_slug: str,
                               session: AsyncSession = Depends(db_helper.scoped_session_dependency)):

    cached_categories = await redis_client.get(REDIS_KEY)
    if cached_categories:
        categories = json.loads(cached_categories)
        for category in categories:
            if category["slug"] == category_slug:
                return category

    category = await crud.get_category_by_slug(session, category_slug)
    if category:
        return AccessoryCategorySchema.model_validate(category)
    return {"error": f"Accessory category with slug {category_slug} was not found"}