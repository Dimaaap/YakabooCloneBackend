from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from review_reactions.schema import ReviewReactionSchema, ReviewReactionCreate
from core.models import db_helper
from . import crud

router = APIRouter(tags=["Review Reactions"])

@router.post("/{review_id}/react", response_model=ReviewReactionCreate)
async def react_to_review(
        review_id: int,
        is_like: bool,
        user_id: int,
        session: AsyncSession=Depends(db_helper.scoped_session_dependency),
):
    reaction = await crud.react_to_review(session,
                                          user_id=user_id,
                                          review_id=review_id,
                                          is_like=is_like)

    if reaction is None:
        return ReviewReactionSchema(
            user_id=user_id,
            review_id=review_id,
            is_like=is_like,
            created_at=None
        )
    return ReviewReactionSchema.from_orm(reaction)


@router.get("/{review_id}/my-reaction", response_model=ReviewReactionSchema | None)
async def get_my_reaction(
        review_id: int,
        user_id: int,
        session: AsyncSession=Depends(db_helper.scoped_session_dependency),
):
    reaction = await crud.get_user_review_reaction(
        session,
        user_id=user_id,
        review_id=review_id
    )

    if reaction is None:
        return None
    return ReviewReactionSchema.from_orm(reaction)