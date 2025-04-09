from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Wishlist, User
from .schemas import WishlistCreate, WishlistUpdatePartial


async def check_user_exists(session: AsyncSession, email: str):
    statement = select(User).where(User.email == email)
    result: Result = await session.execute(statement)
    user = result.scalars().first()
    return user


async def create_wishlist(session: AsyncSession,
                          wishlist: WishlistCreate, email: str) -> Wishlist:
    check_user = await check_user_exists(session, email)
    if not check_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email {email} was not found")

    new_wishlist = Wishlist(title=wishlist.title, is_active=wishlist.is_active)
    new_wishlist.user_id = check_user.id

    try:
        session.add(new_wishlist)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return new_wishlist


async def get_all_wishlists_by_user_email(session: AsyncSession, email: str) -> list[Wishlist]:
    check_user = await check_user_exists(session, email)

    if not check_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email {email} was not found")

    user_id = check_user.id
    statement = select(Wishlist).where(Wishlist.user_id == user_id)
    result: Result = await session.execute(statement)
    wishlists = result.scalars().all()
    return list(wishlists)


async def delete_wishlist_by_id(session: AsyncSession, wishlist_id: int) -> bool | None:
    try:
        statement = select(Wishlist).where(Wishlist.id == wishlist_id)
        result: Result = await session.execute(statement)
        wishlist = result.scalars().first()
        if wishlist:
            await session.delete(wishlist)
            await session.commit()
            return True
    except SQLAlchemyError as e:
        await session.rollback()
        raise e


async def update_wishlist_title(session: AsyncSession, wishlist_id: int,
                                wishlist_data: WishlistUpdatePartial) -> Wishlist:

    try:
        statement = select(Wishlist).where(Wishlist.id == wishlist_id)
        result: Result = await session.execute(statement)
        wishlist = result.scalars().first()

        if not wishlist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Wishlist with id {wishlist_id} was not found")

        if wishlist_data.title:
            wishlist.title = wishlist_data.title

        await session.commit()
        await session.refresh(wishlist)
        return wishlist
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


