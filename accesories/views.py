from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from accesories.schemas import AccessoriesSchema, AccessoriesCreate
from core.models import db_helper
from . import crud

router = APIRouter(tags=["Accessories"])


@router.get("/all", response_model=list[AccessoriesSchema])
async def get_all_accessories(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    accessories = await crud.get_all_accessories(session)
    return accessories


@router.get("/by-slug/{slug}", response_model=AccessoriesSchema)
async def get_accessory_by_slug(
        slug: str,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    accessory = await crud.get_accessory_by_slug(session, slug)
    return accessory


@router.get("/{accessory_id}", response_model=AccessoriesSchema)
async def get_accessory_by_id(
        accessory_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    accessory = await crud.get_accessory_by_id(session, accessory_id)
    return accessory


@router.get('/brand-slug/{brand_slug}', response_model=list[AccessoriesSchema])
async def get_all_accessories_by_brand_slug(brand_slug: str,
                                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    accessories = await crud.get_all_accessories_by_brand_slug(session, brand_slug)
    return accessories


@router.delete("/{accessory_id}")
async def delete_accessory(accessory_id: int,
                           session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    success = await crud.delete_accessory_by_id(session, accessory_id)

    if success:
        return {"message": f"The accessory with id { accessory_id } has been deleted"}
    return {"message": "Deleting failed"}