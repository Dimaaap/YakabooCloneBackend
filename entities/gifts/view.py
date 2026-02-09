import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..gifts.schemas import GiftSchema, GiftCreate
from core.models import db_helper
from . import crud

router = APIRouter(tags=["Gifts"])


@router.post("/create")
async def create_gift(gift_data: GiftCreate, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    gift = await crud.create_gift(session, gift_data)
    return gift



@router.get("/all", response_model=list[GiftSchema])
async def get_all_gifts(session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    gifts = await crud.get_all_gifts(session)
    return gifts


@router.get('/by-slug/{slug}', response_model=GiftSchema)
async def get_gift_by_slug(
        slug: str,
        session: AsyncSession=Depends(db_helper.scoped_session_dependency)
):
    gift = await crud.get_gift_by_slug(session, slug)
    return gift


@router.get("/{gift_id}", response_model=GiftSchema)
async def get_gift_by_id(
        gift_id: int,
        session: AsyncSession=Depends(db_helper.scoped_session_dependency)
):
    gift = await crud.get_gift_by_id(session, gift_id)
    return gift


@router.delete("/{gift_id}")
async def delete_gift_by_id(
        gift_id: int,
        session: AsyncSession=Depends(db_helper.scoped_session_dependency)
):
    success = await crud.delete_gift_by_id(session, gift_id)

    if success:
        return {"message": f"The gift with id {gift_id} has been deleted"}
    else:
        return {"message": "Deleting Error"}
