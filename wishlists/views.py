from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import WishlistSchema, WishlistCreate, WishlistUpdatePartial
from core.models import db_helper
from . import crud

router = APIRouter(tags=["wishlists"])


@router.get("/{user_email}", response_model=list[WishlistSchema])
async def get_wishlists_by_user_id(
        user_email: str,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_all_wishlists_by_user_email(session, user_email)


@router.post("/create", response_model=WishlistSchema)
async def create_wishlist(
        wishlist: WishlistCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.create_wishlist(session, wishlist, wishlist.email)


@router.delete("/{wishlist_id}")
async def delete_wishlist(
    wishlist_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.delete_wishlist_by_id(session, wishlist_id)


@router.put("/{wishlist_id}", response_model=WishlistSchema)
async def update_wishlist(
        wishlist_id: int,
        wishlist_data: WishlistUpdatePartial,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    updated_wishlist = await crud.update_wishlist_title(session=session, wishlist_id=wishlist_id,
                                                        wishlist_data=wishlist_data)
    return updated_wishlist