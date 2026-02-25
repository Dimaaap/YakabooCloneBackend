from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.review_reactions.schema import ReviewReactionsForAdminList
from core.models import ReviewReaction


async def get_review_reactions_for_admin_page(session: AsyncSession) -> list[ReviewReactionsForAdminList]:
    statement = (
        select(ReviewReaction)
        .options(
            joinedload(ReviewReaction.user),
            joinedload(ReviewReaction.review)
        )
        .order_by(ReviewReaction.id)
    )

    result = await session.execute(statement)
    review_reactions = result.unique().scalars().all()

    for reaction in review_reactions:
        reaction.user_email = reaction.user.email
        reaction.review_title = reaction.review.title if reaction.review.title else None

    return [
        ReviewReactionsForAdminList.model_validate(reaction)
        for reaction in review_reactions
    ]
