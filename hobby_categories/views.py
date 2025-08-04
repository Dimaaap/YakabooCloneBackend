import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from banners.views import SIX_DAYS
from .schemas import HobbyCategorySchema, HobbyCategoryCreate
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["Hobby Categories"])

REDIS_KEY = "hobby_categories"


@router.get("/all", response_model=list[HobbyCategorySchema])
async def get_all_hobby_categories(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_categories = await redis_client.get(REDIS_KEY)

    if cached_categories:
        return json.loads(cached_categories)

    categories = await crud.get_all_hobby_categories(session)
    await redis_client.set(REDIS_KEY, json.dumps([category.model_dump() for category in categories]), ex=SIX_DAYS)
    return categories


@router.get("/{slug}", response_model=HobbyCategorySchema)
async def get_hobby_category_by_slug(slug: str, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_categories = await redis_client.get(REDIS_KEY)

    if cached_categories:
        categories_list = json.loads(cached_categories)

        for category in categories_list:
            if category["slug"] == slug:
                return category
    else:
        categories = await crud.get_all_hobby_categories(session)
        await redis_client.set(REDIS_KEY, json.dumps([category.model_dump() for category in categories]), ex=SIX_DAYS)
        return await crud.get_hobby_category_by_slug(session, slug)


@router.get("/{category_id}", response_model=HobbyCategorySchema)
async def get_hobby_category_by_id(category_id: int,
                                   session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_categories = await redis_client.get(REDIS_KEY)

    if cached_categories:
        categories_list = json.loads(cached_categories)
        for category in categories_list:
            if category["id"] == category_id:
                return category
    else:
        categories = await crud.get_all_hobby_categories(session)
        await redis_client.set(REDIS_KEY,
                                json.dumps([category.model_dump() for category in categories]), ex=SIX_DAYS)
        return await crud.get_hobby_category_by_id(session, category_id)


@router.post("/create")
async def create_hobby_category(hobby_category: HobbyCategoryCreate,
                                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_category = await crud.create_hobby_category(session, hobby_category)

    if new_category:
        await redis_client.delete(REDIS_KEY)
        return new_category

    return {"message": "Error while creating creating hobby category"}


@router.delete("/{category_id}")
async def delete_hobby_category_by_id(category_id: int,
                                      session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    deleted_category = await crud.delete_hobby_category_by_id(session, category_id)
    if deleted_category:
        await redis_client.delete(REDIS_KEY)
        return {"message": f"The hobby category with id {category_id} was deleted"}
    return {"error": deleted_category}
