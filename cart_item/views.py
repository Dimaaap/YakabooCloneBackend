from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud

router = APIRouter(tags=["Cart Items"])


@router.post("/add")
async def add_cart_item_to_cart(book_id: int, user_email: str, quantity: int = 1,
                                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.add_item_to_card(session, book_id, user_email, quantity)


@router.patch("/update")
async def update_cart_item_quantity(book_id: int, user_email: str, quantity,
                                    session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.update_book_quantity(session, book_id, quantity, user_email)


@router.delete("/delete")
async def delete_from_cart(book_id: int, user_email: str,
                           session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.delete_item_from_cart(session, book_id, user_email)

