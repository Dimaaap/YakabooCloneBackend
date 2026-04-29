from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .schema import CartItemCreate, CartItemSchema
from entities.users.crud import get_user_by_email
from core.models import Book, CartItem, Cart


async def add_item_to_card(session: AsyncSession, book_id: int, user_email: str,
                           quantity: int = 1) -> CartItemCreate:

    if quantity < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than 0"
        )

    try:
        user = await get_user_by_email(session, user_email)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        cart = user.cart

        if not cart:
            cart = Cart(user_id=user.id)
            session.add(cart)
            await session.flush()

        book = await session.scalar(
            select(Book).where(Book.id == book_id)
        )

        if not book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book not found"
            )
        cart_item = await session.scalar(
            select(CartItem).where(
                CartItem.cart_id == cart.id,
                CartItem.book_id == book.id
            )
            .with_for_update()
        )

        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(
                book_id=book.id,
                cart_id=cart.id,
                quantity=quantity
            )
            session.add(cart_item)
        await session.commit()
        await session.refresh(cart_item)

        return CartItemSchema.model_validate(cart_item)

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )


async def update_book_quantity(session: AsyncSession, book_id: int, quantity: int,
                               user_email: str):
    user = await get_user_by_email(session, user_email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cart_statement = select(Cart).where(Cart.user_id == user.id)
    result = await session.execute(cart_statement)
    cart = result.unique().scalar_one_or_none()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    result = await session.execute(select(CartItem).where(CartItem.cart_id == cart.id,
                                                          CartItem.book_id == book_id))

    cart_item = result.scalar_one_or_none()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Book not found in the cart")

    if int(quantity) <= 0:
        await session.delete(cart_item)
    else:
        cart_item.quantity = int(quantity)
    await session.commit()
    return {"message": "Cart item updated"}


async def delete_item_from_cart(session: AsyncSession, book_id: int, user_email: str):
    user = await get_user_by_email(session, user_email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    statement = select(Cart).where(Cart.user_id == user.id)
    result = await session.execute(statement)
    cart = result.scalar_one_or_none()

    if not cart:
        raise HTTPException(status_code=404, detail="Book not found")

    cart_item_statement = select(CartItem).where(CartItem.cart_id == cart.id, CartItem.book_id == book_id)
    result = await session.execute(cart_item_statement)
    cart_item = result.unique().scalar_one_or_none()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Book not found in the cart")

    await session.delete(cart_item)
    await session.commit()
    return {"message": f"Book with id {book_id} has been deleted"}