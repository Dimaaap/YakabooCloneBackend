from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AdditionalTextBase(BaseModel):
    text: str
    active: bool = True


class AdditionalTextCreate(AdditionalTextBase):
    created_at: datetime | None = None
    updated_at: datetime | None = None


class AdditionalTextUpdate(AdditionalTextCreate):
    ...


class AdditionalTextUpdatePartial(AdditionalTextUpdate):
    text: str | None = None


class AdditionalTextSchema(AdditionalTextBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
