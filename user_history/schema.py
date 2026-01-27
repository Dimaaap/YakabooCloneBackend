from datetime import datetime

from pydantic import BaseModel, ConfigDict

from users.schemas import UserSchema


class UserHistoryBase(BaseModel):
    term: str
    is_active: bool = True

    user_id: int | None = None


class UserHistoryCreate(UserHistoryBase):
    ...


class UserHistoryUpdate(UserHistoryCreate):
    ...


class UserHistoryUpdatePartial(UserHistoryUpdate):
    term: str | None = None


class UserHistorySearchSchema(UserHistoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user: UserSchema