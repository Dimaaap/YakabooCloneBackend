from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Reviews(BaseModel):
    rate: int = 5
    title: str | None = None
    comment: str
    user_name: str
    created_date: datetime | None = None
    is_validated: bool = False
    likes_count: int = 0
    disliked_count: int = 0

    user_email: str
    book_title: str


class ReviewsForAdminList(Reviews):
    model_config = ConfigDict(from_attributes=True)