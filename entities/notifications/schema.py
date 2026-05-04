from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, field_validator


class NotificationBase(BaseModel):
    title: str
    description: str | None = None
    image_src: str | None = None
    link: str | None = None
    is_global: bool = True
    expires_at: datetime | None = None
    is_active: bool = True

    @field_validator("expires_at")
    @classmethod
    def validate_expiry(cls, value):
        if not value:
            return value
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)

        if value < now:
            raise ValueError("expires_at can`t be in the past")
        return value



class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(NotificationCreate):
    pass


class NotificationUpdatePartial(NotificationUpdate):
    title: str | None = None


class NotificationSchema(NotificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_read: bool = False
    user_ids: list[int] | None = None
    created_at: datetime