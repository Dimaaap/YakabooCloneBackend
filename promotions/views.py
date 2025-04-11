from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import PromotionSchema, PromotionCreate
from core.models import db_helper
from . import crud

router = APIRouter(tags=["promotions"])


@router.get("/all", response_model=list[PromotionSchema])
async def get_all_promotions(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.get_all_promotions(session)


@router.get("/{promotion_slug}", response_model=PromotionSchema)
async def get_promotion_by_slug(promotion_slug: str,
                                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.get_promotions_by_slug(promotion_slug, session)


@router.get("/{promotion_id}", response_model=PromotionSchema)
async def get_promotion_by_id(promotion_id: int,
                              session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.get_promotion_by_id(promotion_id, session)


@router.get("/category/{category_id}", response_model=list[PromotionSchema])
async def get_all_promotions_by_category_id(category_id: int,
                                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    print("here")
    return await crud.get_all_promotions_by_category_id(session, category_id)


@router.get("/category/{category_slug}", response_model=list[PromotionSchema])
async def get_all_promotions_by_category_slug(category_slug: str,
                                              session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.get_all_promotions_by_category_slug(session, category_slug)


@router.get("/category/promotions")
async def get_all_promotions_with_categories(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.get_all_promotions_with_categories(session)


@router.delete("/{promo_id}")
async def delete_promotion_by_id(
        promo_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    deleted = await crud.delete_promotion_by_id(promo_id, session)
    if deleted:
        return {"message": f"Promotion with id {promo_id} has been deleted"}
    return {"message": "Error while deleting"}


@router.post("/create")
async def create_promotion(
        promo: PromotionCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> PromotionSchema:
    promotion = await crud.create_promotion(session, promo)
    return promotion


