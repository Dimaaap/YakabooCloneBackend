from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import AccessoryCategorySchema, AccessoryCategoryCreate
from core.models import db_helper
from . import crud

router = APIRouter(tags=["Accessory Categories"])

@router.get("/all", response_model=list[AccessoryCategorySchema])
async def get_all_categories(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    categories = await crud.get_all_categories(session)
    return categories


@router.get("/create")
async def create_category(
        category: AccessoryCategoryCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    new_category = await crud.create_accessory_category(session, category)
    if new_category:
        return new_category
    return {"message": "Error creating accessory category"}


@router.delete("/{accessory_category_id}")
async def delete_category(
        accessory_category_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    category = await crud.delete_category_by_id(session, accessory_category_id)
    if category:
        return {"message": f"Accesory category {accessory_category_id} deleted"}
    return {"error": category}