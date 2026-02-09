from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import AccessoryBrandSchema, AccessoryBrandCreate, AccessoryBrandWithCountSchema
from core.models import db_helper
from . import crud

router = APIRouter(tags=["Accessory Brands"])


@router.get("/all", response_model=list[AccessoryBrandWithCountSchema])
async def get_all_brands(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    brands = await crud.get_all_brands(session)
    return brands


@router.get("/search/", response_model=list[AccessoryBrandSchema])
async def search_brands(
        query: str = Query(...),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    brands = await crud.get_brand_by_query(query, session)
    return brands


@router.post("/create")
async def create_accessory_brand(
        brand: AccessoryBrandCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    new_brand = await crud.create_accessory_brand(session, brand)
    if new_brand:
        return new_brand
    return {"message": "Error while creating the accessory brand"}


@router.delete("/{accessory_brand_id}")
async def delete_accessory_brand(
        brand_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    brand = await crud.delete_brand_by_id(session, brand_id)
    if brand:
        return {"message": f"Accessory brand with id {brand_id} was deleted"}
    return {"error": brand}


@router.get("/accessories/{brand_slug}")
async def get_brand_by_id(brand_slug: str,
                          session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    brand = await crud.get_all_accessories_by_brand_slug(brand_slug, session)

    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")
    return brand


@router.get("/by-slug/{brand_slug}")
async def get_brand_by_slug(brand_slug: str,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    brand = await crud.get_brand_by_slug(session, brand_slug)
    if brand:
        return AccessoryBrandSchema.model_validate(brand)
    return {"error": f"Accessory brand with slug {brand_slug} was not found"}