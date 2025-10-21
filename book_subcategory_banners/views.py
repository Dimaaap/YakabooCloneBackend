import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .schema import BookSubcategoryBannerSchema, BookSubcategoryBannerCreate
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["Book Subcategory Banners"])
REDIS_KEY = "book_subcategory_banners"


@router.get("/all", response_model=list[BookSubcategoryBannerSchema])
async def get_all_book_subcategory_banners(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_banners = await redis_client.get(REDIS_KEY)

    if cached_banners:
        return json.loads(cached_banners)

    banners = await crud.get_all_book_subcategory_banners(session)
    await redis_client.set(REDIS_KEY, json.dumps([banner.model_dump() for banner in banners]))
    return banners


@router.get("/{slug}", response_model=BookSubcategoryBannerSchema)
async def get_book_subcategory_banner_by_slug(slug: str,
                                              session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_banners = await redis_client.get(REDIS_KEY)

    if cached_banners:
        banners_list = json.loads(cached_banners)

        for banner in banners_list:
            if banner["slug"] == slug:
                return banner

    else:
        banners = await crud.get_all_book_subcategory_banners(session)
        await redis_client.set(REDIS_KEY, json.dumps([banner.model_dump() for banner in banners]))
        return await crud.get_book_subcategory_banner_by_slug(session, slug)


@router.post("/create")
async def create_book_subcategory_banner(book_subcategory_banner: BookSubcategoryBannerCreate,
                                         session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_banner = await crud.create_book_subcategory_banner(session, book_subcategory_banner)

    if new_banner:
        await redis_client.delete(REDIS_KEY)
        return new_banner

    return {"message": "Error while creating a new book subcategory banner"}


@router.delete("/{banner_id}")
async def delete_book_subcategory_banner_by_id(subcategory_banner_id: int,
                                               session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    deleted_banner = await crud.delete_book_subcategory_banner_by_id(session, subcategory_banner_id)

    if deleted_banner:
        await redis_client.delete(REDIS_KEY)
        return {"message": f"The book subcategory banner with id {subcategory_banner_id} was been deleted"}

    return {"message": deleted_banner}
