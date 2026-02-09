from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import PromoCategorySchema, PromoCategoryCreate
from core.models import db_helper
from . import crud

router = APIRouter(tags=["promotion categories"])


@router.get("/all", response_model=list[PromoCategorySchema])
async def get_all_promotion_categories(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_all_promotion_categories(session)


@router.delete("/{category_id}")
async def delete_promotion_category(
        category_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    deleted = await crud.delete_promo_category(session=session, category_id=category_id)
    if deleted:
        return {"message": f"Promotion category with id {category_id} has been deleted"}
    return {"message": "Error while deleting"}


@router.post("/create", response_model=PromoCategoryCreate)
async def create_promotion_category(
        promo_category: PromoCategoryCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    category = await crud.create_promotion_category(session, promo_category)
    return category