from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.reviews.schema import ReviewsForAdminList, EditReview
from core.models import Review


async def get_reviews_list_for_admin_page(session: AsyncSession) -> list[ReviewsForAdminList]:
    statement = (
        select(Review)
        .options(
            joinedload(Review.user),
            joinedload(Review.book)
        )
        .order_by(Review.id)
    )

    result = await session.execute(statement)
    reviews = result.unique().scalars().all()

    for review in reviews:
        review.user_email = review.user.email
        review.book_title = review.book.title

    return [
        ReviewsForAdminList.model_validate(review)
        for review in reviews
    ]


async def get_reviews_field_data(session: AsyncSession, review_slug: str) -> ReviewsForAdminList:
    statement = (
        select(Review)
        .options(
            joinedload(Review.user),
            joinedload(Review.book)
        )
        .where(Review.title == review_slug)
    )

    result = await session.execute(statement)
    review = result.scalars().first()
    review.user_email = review.user.email
    review.book_title = review.book.title

    return ReviewsForAdminList.model_validate(review)


async def get_review_by_slug(session: AsyncSession, review_slug: str) -> Review | bool:
    review = await session.get(Review, review_slug)

    if not review:
        return False

    return review


async def update_review(session: AsyncSession, review_slug: str, data: EditReview) -> bool:
    review = await get_review_by_slug(session, review_slug)

    if not review:
        raise NotFoundInDbError("Review not found")

    update_data = data.model_dump(exclude_uset=True)

    for field, value in update_data.items():
        setattr(review, field, value)

    await session.commit()

    return True
