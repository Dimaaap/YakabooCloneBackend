from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReviewReactionsBase(BaseModel):
    user_id: int
    review_id: int
    is_like: bool = False
    created_at: datetime | None = None


class ReviewReactionCreate(ReviewReactionsBase):
    ...


class ReviewReactionUpdate(ReviewReactionCreate):
    ...


class ReviewReactionUpdatePartial(ReviewReactionUpdate):
    user_id: int | None = None
    review_id: int | None = None
    is_like: bool | None = None


class ReviewReactionSchema(ReviewReactionsBase):
    model_config = ConfigDict(from_attributes=True)

    id: int