from datetime import datetime

from pydantic import BaseModel, ConfigDict

from entities.users.schemas import UserSchema
from entities.books.schemas import BookSchema


class UserSeenBooksBase(BaseModel):
    user_id: int
    book_id: int

    seen_date: datetime


class UserSeenBooksCreate(UserSeenBooksBase):
    ...


class UserSeenBooksUpdate(UserSeenBooksCreate):
    ...


class UserSeenBooksUpdatePartial(UserSeenBooksUpdate):
    user_id: int | None = None
    book_id: int | None = None

    seen_date: datetime | None = None


class UserSeenBooksSchema(UserSeenBooksBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user: UserSchema
    book: BookSchema