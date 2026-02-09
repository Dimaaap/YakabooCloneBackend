import json

from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..banners.views import SIX_DAYS
from .schemas import GiftBrandSchema, GiftBrandCreate
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["Gift Brands"])
REDIS_KEY = "gift_brands"


@router.get("/all", response_model=list[GiftBrandSchema])
async def get_all_brands(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_brands = await redis_client.get(REDIS_KEY)

    if cached_brands:
        return json.loads(cached_brands)

    brands = await crud.get_all_brands(session)
    await redis_client.set(REDIS_KEY, json.dumps([brand.model_dump() for brand in brands]),
                           ex=SIX_DAYS)
    return brands


@router.post("/create")
async def create_brand(brand: GiftBrandCreate,
                       session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_brand = await crud.create_gift_brand(session, brand)
    if new_brand:
        await redis_client.delete(REDIS_KEY)
        return new_brand
    return {"error": "Error while creating gift brand"}


@router.get("/search", response_model=list[GiftBrandSchema])
async def search_brands(
        query: str = Query(...),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    brands = await crud.get_brand_by_query(query, session)
    return brands


@router.delete("/{gift_brand_id}")
async def delete_brand(gift_brand_id: int,
                       session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_brands = await redis_client.get(REDIS_KEY)
    if cached_brands:
        for brand in json.loads(cached_brands):
            if brand["id"] == gift_brand_id:
                list(json.loads(cached_brands)).remove(brand)
    brand = await crud.delete_brand_by_id(session, gift_brand_id)
    if brand:
        return {"message": f"The gift brand with id {gift_brand_id} was deleted"}
    return {"error": brand}


@router.get("/{brand_id}")
async def get_brand_by_id(brand_id: int,
                          session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_brands = await redis_client.get(REDIS_KEY)
    if cached_brands:
        for brand in json.loads(cached_brands):
            if brand["id"] == brand_id:
                return brand
    brand = await crud.get_brand_by_id(session, brand_id)
    if brand:
        return GiftBrandSchema.model_validate(brand)
    return {"error": f"Gift brand with id {brand_id} was not found"}


@router.get("/gifts/{brand_slug}")
async def get_gifts_by_brand_slug(brand_slug: str,
                                  session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    brand = await crud.get_all_gifts_by_brand_slug(brand_slug, session)

    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand was not found")
    return brand


@router.get("/by-slug/{brand_slug}")
async def get_brand_by_slug(brand_slug: str,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_brand = await redis_client.get(REDIS_KEY)
    if cached_brand:
        for brand in json.loads(cached_brand):
            if brand["slug"] == brand_slug:
                return brand
    brand = await crud.get_brand_by_slug(session, brand_slug)
    if brand:
        return GiftBrandSchema.model_validate(brand)
    return {"error": f"Gift brand with slug {brand_slug} was not found"}



