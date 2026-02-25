from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.reviews.schema import ReviewsForAdminList
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
