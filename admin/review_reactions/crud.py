from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.review_reactions.schema import ReviewReactionsForAdminList, EditReviewReaction
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


async def get_review_reactions_field_data(session: AsyncSession, reaction_id: int) -> ReviewReactionsForAdminList:
    statement = (
        select(ReviewReaction)
        .options(
            joinedload(ReviewReaction.user),
            joinedload(ReviewReaction.review)
        )
        .where(ReviewReaction.id == reaction_id)
    )

    result = await session.execute(statement)
    reaction = result.scalars().first()

    reaction.user_email = reaction.user.email
    reaction.review_title = reaction.review.title if reaction.review.title else None
    return ReviewReactionsForAdminList.model_validate(reaction)


async def get_review_reaction_by_id(session: AsyncSession, reaction_id: int) -> ReviewReaction | bool:
    review_reaction = await session.get(ReviewReaction, reaction_id)

    if not review_reaction:
        return False

    return review_reaction


async def update_review_reaction(session: AsyncSession, reaction_id: int, data: EditReviewReaction) -> bool:
    review_reaction = await get_review_reaction_by_id(session, reaction_id)

    if not review_reaction:
        raise NotFoundInDbError("Review Reaction not found")

    update_data = data.model_dump(exclude_uset=True)

    for field, value in update_data.items():
        setattr(review_reaction, field, value)

    await session.commit()

    return True