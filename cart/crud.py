from fastapi import HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from users.crud import get_user_by_email
from core.models import CartItem, Cart


async def get_cart(session: AsyncSession, user_email: str):
    user = await get_user_by_email(session, user_email)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    cart_statement = (select(Cart).where(Cart.user_id == user.id)
                      .options(selectinload(Cart.items).joinedload(CartItem.book)))
    result = await session.execute(cart_statement)
    cart = result.scalar_one_or_none()

    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User`s cart not found")

    return {
        "items": [
            {
                "book_id": item.book_id,
                "title": item.book.title,
                "price": item.book.price,
                "images": item.book.images,
                "slug": item.book.slug,
                "is_in_stock": item.book.book_info.in_stock,
                "format": item.book.book_info.format,
                "code": item.book.book_info.code,
                "quantity": item.quantity,
                "authors": item.book.authors,
                "total": item.book.price * item.quantity

            }
            for item in cart.items
        ],
        "total_price": sum(item.book.price * item.quantity for item in cart.items)
    }


async def clear_cart(session: AsyncSession, user_email: str):
    user = await get_user_by_email(session, user_email)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    cart_statement = select(Cart).where(Cart.user_id == user.id)
    result = await session.execute(cart_statement)
    cart = result.scalar_one_or_none()

    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User`s cart not found")

    statement = delete(CartItem).where(CartItem.cart_id == cart.id)
    await session.execute(statement)
    await session.commit()
    return {"message": "Cart cleared"}