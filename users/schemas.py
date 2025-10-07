from datetime import date, datetime
from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, ConfigDict, StringConstraints

from core.models.user import UserStatusEnum


class UserBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: Annotated[str, StringConstraints(min_length=8)]
    email: EmailStr
    bonuses: int
    level: UserStatusEnum | None = None


class UserWithoutPassword(UserBase):
    is_active: bool
    date_joined: datetime
    is_staff: bool
    is_verified: bool
    id: int


class UserCreate(UserBase):
    password: str
    agree: bool | None = True


class UserRegister(BaseModel):
    user: UserCreate


class VerifyCodeRequest(BaseModel):
    phone_number: str
    code: str


class VerifyCodeReturn(UserRegister):
    access_token: str
    refresh_token: str
    token_type: str


class UserUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    birth_date: Optional[date] = None


class UserSchema(UserBase):
    model_config = ConfigDict(from_attributes=True)

    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    password: bytes | None = None
    email: EmailStr | None = None
    is_active: bool | None = True
    is_staff: bool | None = False
    agree: bool | None = True
    is_verified: bool | None = False


class ChangePasswordBody(BaseModel):
    user_email: str
    current_password: str
    new_password: str


class ChangePasswordWithEmail(BaseModel):
    user_email: EmailStr


class ChangeUserSubscriptionToNews(BaseModel):
    phone_number: str
    is_subscribed_to_news: bool


class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    user: UserSchema
    access_token: str
    refresh_token: str
    token_type: str


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr | None = None 