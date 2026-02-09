import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..banners.views import SIX_DAYS
from .schemas import GiftSubcategorySchema, GiftSubcategoryCreate
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["Gift Subcategories"])

REDIS_KEY = "gift_subcategories"


@router.get("/all", response_model=list[GiftSubcategorySchema])
async def get_all_gift_subcategories(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_subcategories = await redis_client.get(REDIS_KEY)

    if cached_subcategories:
        return json.loads(cached_subcategories)

    subcategories = await crud.get_all_gift_subcategories(session)
    await redis_client.set(REDIS_KEY, json.dumps([sub.model_dump() for sub in subcategories]),
                           ex=SIX_DAYS)
    return subcategories


@router.get("/{slug}", response_model=GiftSubcategorySchema)
async def get_gift_subcategory_by_slug(slug: str,
                                        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_subcategories = await redis_client.get(REDIS_KEY)

    if cached_subcategories:
        sub_list = json.loads(cached_subcategories)

        for sub in sub_list:
            if sub["slug"] == slug:
                return sub
    else:
        subcategories = await crud.get_all_gift_subcategories(session)
        await redis_client.set(REDIS_KEY, json.dumps([sub.model_dump() for sub in subcategories]))
        return await crud.get_gift_subcategory_by_slug(session, slug)


@router.get("/gifts/{slug}")
async def get_gifts_by_subcategory_slug(slug: str,
                                          session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    subcategory = await crud.get_gifts_by_subcategory_slug(session, slug)
    return subcategory


@router.get("/by-id/{subcategory_id}", response_model=GiftSubcategorySchema)
async def get_gift_subcategory_by_id(subcategory_id: int,
                                      session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_subcategories = await redis_client.get(REDIS_KEY)

    if cached_subcategories:
        sub_list = json.loads(cached_subcategories)
        for sub in sub_list:
            if sub["id"] == subcategory_id:
                return sub
    else:
        sub_list = await crud.get_all_gift_subcategories(session)
        await redis_client.set(REDIS_KEY, json.dumps([sub.model_dump() for sub in sub_list]))
        return await crud.get_gift_subcategory_by_id(session, subcategory_id)


@router.post("/create") 
async def create_gity_subcategory(gift_subcategory: GiftSubcategoryCreate,
                                   session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_subcategory = await crud.create_gift_subcategory(session, gift_subcategory)

    if new_subcategory:
        await redis_client.delete(REDIS_KEY)
        return new_subcategory

    return {"message": "Error while creating new gift subcategory"}


@router.delete("/{subcategory_id}")
async def delete_gift_subcategory_by_id(subcategory_id: int,
                                         session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    deleted_subcategory = await crud.delete_gift_subcategory_by_id(session, subcategory_id)

    if deleted_subcategory:
        await redis_client.delete(REDIS_KEY)
        return {"message": f"The gift subcategory with id { subcategory_id } was deleted"}

    return {"error": deleted_subcategory}
