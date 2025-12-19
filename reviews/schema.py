from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReviewBase(BaseModel):
    rate: int = 5
    title: str | None = None
    comment: str
    created_date: datetime = datetime.now()
    is_validated: bool = True
    user_id: int
    book_id: int


class ReviewCreate(ReviewBase):
    ...


class ReviewUpdate(ReviewCreate):
    ...


class ReviewUpdatePartial(ReviewUpdate):
    rate: int | None = None
    comment: str | None = None
    created_date: datetime | None = None
    is_validated: bool | None = None
    user_id: int | None = None
    book_id: int | None = None


class ReviewSchema(ReviewBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

