from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .schema import PromoCodeUsageSchema

router = APIRouter(tags=["Promo Codes Usage"])


@router.post("/use")
async def use_promo_code(user_id: int, code: str,
                         session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    return await crud.use_promo_code(session, user_id, code)


@router.get("/all/{user_id}", response_model=list[PromoCodeUsageSchema])
async def get_all_promo_usages(
        user_id: int,
        session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    return await crud.get_all_promo_usages(session, user_id)


@router.get("/{promo_code_id}")
async def get_usage_by_code_id(promo_code_id: int,
                               session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    return await crud.get_usages_by_promo(session, promo_code_id)
