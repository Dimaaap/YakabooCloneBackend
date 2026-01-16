from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReviewBase(BaseModel):
    rate: int = 5
    title: str | None = None
    comment: str
    user_name: str
    likes_count: int = 0
    dislikes_count: int = 0
    created_date: datetime = datetime.now()
    is_validated: bool = True
    user_email: str | None = None
    book_id: int


class ReviewCreate(ReviewBase):
    ...


class ReviewUpdate(ReviewCreate):
    ...


class ReviewUpdatePartial(ReviewUpdate):
    rate: int | None = None
    comment: str | None = None
    user_name: str | None = None
    created_date: datetime | None = None
    is_validated: bool | None = None
    likes_count: int | None = None
    dislikes_count: int | None = None
    book_id: int | None = None


class ReviewSchema(ReviewBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

