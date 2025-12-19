from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from reviews.schema import ReviewSchema, ReviewCreate
from core.models import db_helper
from . import crud

router = APIRouter(tags=["Reviews for Books"])


@router.post("/create", response_model=ReviewSchema)
async def create_review(
        review: ReviewCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.create_review(session, review)


@router.get('/all', response_model=list[ReviewSchema])
async def get_all_reviews(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_all_reviews(session)


@router.get("/{review_id}", response_model=ReviewSchema)
async def get_review_by_id(
        review_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_review_by_id(session, review_id)


@router.get("/user/{user_id}/reviews", response_model=list[ReviewSchema])
async def get_reviews_by_user_id(
        user_id: int,
        session: AsyncSession=Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_all_reviews_by_user_id(session, user_id)


@router.get("/book/{book_id}/reviews", response_model=list[ReviewSchema])
async def get_all_reviews_for_book(
        book_id: int,
        session: AsyncSession=Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_all_reviews_by_book_id(session, book_id)


@router.delete("/{review_id}")
async def delete_review(
        review_id: int,
        session: AsyncSession=Depends(db_helper.scoped_session_dependency)
):
    return await crud.delete_review_by_id(session, review_id)


@router.delete("user/{user_id}/reviews")
async def delete_all_user_reviews(
        user_id: int,
        session: AsyncSession=Depends(db_helper.scoped_session_dependency)
):
    return await crud.delete_all_users_review(session, user_id)


@router.delete("book/{book_id}/reviews")
async def delete_all_reviews_for_book(
        book_id: int,
        session: AsyncSession=Depends(db_helper.scoped_session_dependency)
):
    return await crud.delete_all_books_review(session, book_id)