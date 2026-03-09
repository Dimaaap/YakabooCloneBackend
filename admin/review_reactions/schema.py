from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReviewReactions(BaseModel):
    user_email: str
    review_title: str

    is_like: bool = False
    created_at: datetime


class ReviewReactionsForAdminList(ReviewReactions):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EditReviewReaction(ReviewReactions):
    user_email: str | None = None
    review_title: str | None = None

    created_at: datetime | None = None