from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from core.models import Review, ReviewReaction


async def react_to_review(session: AsyncSession,
                          *,
                          user_id: int,
                          review_id: int,
                          is_like: bool) -> ReviewReaction | None:
    try:
        review = await session.get(Review, review_id)

        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review does not exist")

        statement = select(ReviewReaction).where(
            ReviewReaction.user_id == user_id,
            ReviewReaction.review_id == review_id
        )

        result = await session.execute(statement)
        reaction = result.scalar_one_or_none()

        if reaction:
            # When user click the same reaction(like / dislike) we need to cancel this reaction
            if reaction.is_like == is_like:
                await session.delete(reaction)

                if is_like:
                    review.likes_count -= 1
                else:
                    review.dislikes_count -= 1
                await session.commit()
                return None
            else:
                # When user click the opposite reaction(from like to dislike or vice versa) need to decrease
                # counter to this reaction and increase an opposite counter
                reaction.is_like = is_like

                if is_like:
                    review.likes_count += 1
                    review.dislikes_count -= 1
                else:
                    review.likes_count -= 1
                    review.dislikes_count +git= 1
        else:
            reaction = ReviewReaction(
                user_id=user_id,
                review_id=review_id,
                is_like=is_like
            )
            session.add(reaction)

            if is_like:
                review.likes_count += 1
            else:
                review.dislikes_count += 1
        await session.commit()
        await session.refresh(reaction)
        return reaction
    except SQLAlchemyError as e:
        await session.rollback()
        raise


async def get_user_review_reaction(
        session: AsyncSession,
        *,
        user_id: int,
        review_id: int
) -> ReviewReaction | None:
    statement = select(ReviewReaction).where(
        ReviewReaction.user_id == user_id,
        ReviewReaction.review_id == review_id
    )

    result = await session.execute(statement)
    return result.scalar_one_or_none()
