from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud

router = APIRouter(tags=["Cart"])

@router.get("/cart-items/all")
async def get_cart(user_email: str, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.get_cart(session, user_email)


@router.post("/clear")
async def clear_cart(user_email: str, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.clear_cart(session, user_email)