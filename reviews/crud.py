from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Review
from .schema import ReviewCreate


async def create_review(session: AsyncSession,
                        review: ReviewCreate) -> Review:
    new_review = Review(**review.model_dump())

    try:
        session.add(new_review)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return new_review


async def get_review_by_id(session: AsyncSession,
                           review_id: int) -> Review:
    statement = select(Review).where(Review.id == review_id)
    result: Result = await session.execute(statement)
    review = result.scalars().first()
    return review


async def get_all_reviews_by_book_id(session: AsyncSession, book_id: int) -> list[Review]:
    statement = select(Review).where(Review.book_id == book_id)
    result: Result = await session.execute(statement)
    reviews = result.scalars().all()
    return list(reviews)


async def get_all_reviews_by_user_id(session: AsyncSession, user_id: int) -> list[Review]:
    statement = select(Review).where(Review.user_id == user_id)
    result: Result = await session.execute(statement)
    reviews = result.scalars().all()
    return list(reviews)


async def delete_review_by_id(session: AsyncSession, review_id: int) -> bool | None:
    try:
        statement = select(Review).where(Review.id == review_id)
        result: Result = await session.execute(statement)
        review = result.scalars().first()
        if review:
            await session.delete(review)
            await session.commit()
            return True
    except SQLAlchemyError as e:
        await session.rollback()
        raise e


async def get_all_reviews(session: AsyncSession) -> list[Review]:
    statement = select(Review).order_by(Review.id)
    result: Result = await session.execute(statement)
    reviews = result.scalars().all()
    return list(reviews)


async def delete_all_users_review(session: AsyncSession, user_id: int):
    try:
        statement = select(Review).where(Review.user_id == user_id)
        result: Result = await session.execute(statement)
        reviews = result.scalars().all()
        if reviews:
            await session.delete(reviews)
            await session.commit()
            return True
    except SQLAlchemyError as e:
        await session.rollback()
        raise e


async def delete_all_books_review(session: AsyncSession, book_id: int):
    try:
        statement = select(Review).where(Review.book_id == book_id)
        result: Result = await session.execute(statement)
        reviews = result.scalars().all()

        if reviews:
            await session.delete(reviews)
            await session.commit()
            return True
    except SQLAlchemyError as e:
        await session.rollback()
        raise e