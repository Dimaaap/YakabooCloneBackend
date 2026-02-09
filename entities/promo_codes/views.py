from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schema import PromoCodeCreate, PromoCodeSchema, PromoCodeUpdate, PromoCodeUpdatePartial
from core.models import db_helper
from . import crud

router = APIRouter(tags=["Promo Codes"])


@router.get("/all", response_model=list[PromoCodeSchema])
async def get_all_promo_codes(session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    return await crud.get_all_promo_codes(session)


@router.post("/create")
async def create_promo_code(promo_code: PromoCodeCreate,
                            session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    return await crud.create_promo_code(session, promo_code)


@router.delete("/{promo_code_id}")
async def delete_promo_code_by_id(promo_code_id: int,
                                  session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.delete_promo_code_by_id(session, promo_code_id)


@router.get("/{code}")
async def get_promo_code_by_code(code: str,
                                 session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    return await crud.get_promo_code_by_code(session, code)


@router.get("/by-id/{promo_code_id}")
async def get_promo_code_by_id(promo_code_id: int,
                               session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    return await crud.get_promo_code_by_id(session, promo_code_id)


@router.put("/{promo_id}", response_model=PromoCodeSchema)
async def update_promo_code(
        promo_id: int,
        promo_data: PromoCodeUpdate,
        session: AsyncSession=Depends(db_helper.scoped_session_dependency)
):
    return await crud.update_promo_code(session, promo_id, promo_data)


@router.patch("/{promo_id}", response_model=PromoCodeSchema)
async def update_promo_code_partial(
        promo_id: int,
        promo_data: PromoCodeUpdatePartial,
        session: AsyncSession=Depends(db_helper.scoped_session_dependency)
):
    return await crud.update_promo_code_partial(session, promo_id, promo_data)



