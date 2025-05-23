import json

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import GameBrandSchema, GameBrandCreate
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["game brands"])

SIX_DAYS = 24 * 36000 * 6


@router.get("/all", response_model=list[GameBrandSchema])
async def get_all_brands(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_brands = await redis_client.get("game_brands")
    if cached_brands:
        return json.loads(cached_brands)

    game_brands = await crud.get_all_brands(session)
    await redis_client.set("game_brands", json.dumps([brand.model_dump() for brand in game_brands]))
    return game_brands


@router.post("/create")
async def create_game_brand(brand: GameBrandCreate,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_brand = await crud.create_game_brand(session, brand)
    if new_brand:
        await redis_client.delete("game_brands")
        return new_brand


@router.delete("/{game_brand_id}")
async def delete_game_brand_by_id(brand_id: int,
                                  session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    deleted_brand = await crud.delete_brand_by_id(brand_id, session)
    if deleted_brand:
        await redis_client.delete("game_brands")
        return {"message": f"The brand with id {brand_id} has been deleted"}
    return {"error": deleted_brand}


@router.get("/{brand_id}")
async def get_brand_by_id(brand_id: int,
                          session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_brands = await redis_client.get("game_brands")

    if cached_brands:
        try:
            brands = json.loads(cached_brands)
            for brand in brands:
                if brand["id"] == brand_id:
                    return GameBrandSchema.model_validate(brand)
        except json.JSONDecodeError:
            pass

    brand = await crud.get_brand_by_id(brand_id, session)
    if brand is None:
        return {"error": f"No brand found with id {brand_id}"}

    return GameBrandSchema.model_validate(brand)


@router.get("/{brand_slug}")
async def get_brand_by_slug(brand_slug: str,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_brands = await redis_client.get("game_brands")

    if cached_brands:
        try:
            brands = json.loads(cached_brands)
            for brand in brands:
                if brand["slug"] == brand_slug:
                    return GameBrandSchema.model_validate(brand)
        except json.JSONDecodeError:
            pass

    brand = await crud.get_brand_by_slug(brand_slug, session)
    if brand is None:
        return {"message": f"No brand found with slug {brand_slug}"}
    return GameBrandSchema.model_validate(brand)
