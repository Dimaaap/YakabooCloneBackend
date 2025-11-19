from datetime import datetime

from pydantic import BaseModel, ConfigDict

from users.schemas import UserSchema
from promo_codes.schema import PromoCodeSchema


class PromoCodeUsageBase(BaseModel):
    user_id: int
    promo_id: int

    used_at: datetime


class PromoCodeUsageCreate(PromoCodeUsageBase):
    ...


class PromoCodeUsageUpdate(PromoCodeUsageCreate):
    ...


class PromoCodeUsageUpdatePartial(PromoCodeUsageUpdate):
    user_id: int | None = None
    promo_id: int | None = None

    used_at: datetime | None = None


class PromoCodeUsageSchema(PromoCodeUsageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user: UserSchema
    promo_code: PromoCodeSchema