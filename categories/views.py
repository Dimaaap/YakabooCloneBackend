from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CategorySchema, SubCategorySchema, CategoryCreate, SubCategoryBase
from core.models import db_helper
from . import crud

router = APIRouter(tags=["categories"])


@router.get("/all", response_model=list[CategorySchema])
async def get_all_categories(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_all_categories(session)


@router.post("/create", response_model=CategorySchema)
async def create_category(
        category: CategoryCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.create_category(session, category)


@router.post("/subcategory/create", response_model=SubCategorySchema)
async def create_subcategory(
        subcategory: SubCategoryBase,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.create_sub_category(session, subcategory)


@router.delete("/{category_id}")
async def delete_category(
        category_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    deleted = await crud.delete_category_by_id(session, category_id)
    if deleted:
        return {"message": f"Category with id {category_id} has been deleted"}
    return {"message": "Server error while deleting"}


@router.delete("/subcategory/{subcategory_id}")
async def delete_subcategory(
        subcategory_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    deleted = await crud.delete_subcategory_by_id(session, subcategory_id)
    if deleted:
        return {"message": f"Subcategory with id {subcategory_id} has been deleted"}
    return {"message": "Server error while deleting"}


@router.get("/subcategories", response_model=list[SubCategorySchema])
async def get_all_subcategories(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_all_subcategories(session)


@router.get("/{category_id}/subcategories", response_model=list[SubCategorySchema])
async def get_all_subcategories_by_category(
        category_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_all_subcategories_by_category_id(session, category_id=category_id)

