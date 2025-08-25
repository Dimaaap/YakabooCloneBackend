from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import AccessoryBrandSchema, AccessoryBrandCreate
from core.models import db_helper
from . import crud

router = APIRouter(tags=["Accessory Brands"])


@router.get("/all", response_model=list[AccessoryBrandSchema])
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