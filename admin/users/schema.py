from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date, datetime

from core.models.user import UserStatusEnum


class UsersList(BaseModel):
    first_name: str
    last_name: str

    phone_number: str
    email: EmailStr
    is_staff: bool | None
    is_active: bool | None
    is_verified: bool | None
    is_subscribed_to_news: bool | None
    birth_date: date | None
    bonuses: int | None
    level: UserStatusEnum

    date_joined: datetime


class UserListForAdmin(UsersList):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: int