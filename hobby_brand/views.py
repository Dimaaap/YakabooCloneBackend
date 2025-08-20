from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import HobbyBrandSchema, HobbyBrandCreate
from core.models import db_helper
from . import crud

router = APIRouter(tags=["Hobby Brands"])


@router.get("/all", response_model=list[HobbyBrandSchema])
async def get_all_brands(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    brands = await crud.get_all_brands(session)
    return brands


@router.get("/search/", response_model=list[HobbyBrandSchema])
async def search_brands(
        query: str = Query(...),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    hobbies = await crud.get_brand_by_query(query, session)
    return hobbies


@router.post("/create")
async def create_hobby_brand(brand: HobbyBrandCreate,
                             session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_brand = await crud.create_hobby_brand(session, brand)
    if new_brand:
        return new_brand
    else:
        return {"message": "Error while creating the hobby brand"}


@router.delete("/{hobby_brand_id}")
async def delete_hobby_brand(brand_id: int,
                             session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    brand = await crud.delete_brand_by_id(session, brand_id)
    if brand:
        return {"message": f"The hobby brand with id {brand_id} was deleted"}
    return {"error": brand}


@router.get("/{brand_id}")
async def get_brand_by_id(brand_id: int,
                          session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    brand = await crud.get_brand_by_id(session, brand_id)
    if brand:
        return HobbyBrandSchema.model_validate(brand)
    return {"error": f"Hobby brand with id {brand_id} was not found"}


@router.get("/hobbies/{brand_slug}")
async def get_hobbies_by_brand_slug(brand_slug: str,
                                    session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    brand = await crud.get_all_hobbies_by_brand_slug(brand_slug, session)

    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand was not found")
    return brand


@router.get("/by-slug/{brand_slug}")
async def get_brand_by_slug(brand_slug: str,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    brand = await crud.get_brand_by_slug(session, brand_slug)
    if brand:
        return HobbyBrandSchema.model_validate(brand)
    return {"error": f"Hobby brand with slug {brand_slug} was not found"}



