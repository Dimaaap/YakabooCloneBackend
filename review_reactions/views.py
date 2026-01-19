from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from review_reactions.schema import ReviewReactionSchema, ReviewReactionResponse
from core.models import db_helper, Review
from . import crud

router = APIRouter(tags=["Review Reactions"])

@router.post("/{review_id}/react", response_model=ReviewReactionResponse)
async def react_to_review(
        review_id: int,
        is_like: bool,
        user_email: str,
        session: AsyncSession=Depends(db_helper.scoped_session_dependency),
):
    reaction = await crud.react_to_review(session,
                                          user_email=user_email,
                                          review_id=review_id,
                                          is_like=is_like)

    review = await session.get(Review, review_id)
    return ReviewReactionResponse(
        id=reaction.id if reaction else None,
        user_email=user_email,
        review_id=review_id,
        is_like=reaction.is_like if reaction else None,
        created_at=reaction.created_at if reaction else None,
        likes_count=review.likes_count,
        dislikes_count=review.dislikes_count
    )


@router.get("/{review_id}/my-reaction", response_model=ReviewReactionSchema | None)
async def get_my_reaction(
        review_id: int,
        user_email: str,
        session: AsyncSession=Depends(db_helper.scoped_session_dependency),
):
    reaction = await crud.get_user_review_reaction(
        session,
        user_email=user_email,
        review_id=review_id
    )

    if reaction is None:
        return None
    return ReviewReactionSchema.from_orm(reaction)