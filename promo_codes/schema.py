from datetime import datetime

from pydantic import BaseModel, ConfigDict

from core.models.promo_code import DiscountTypes


class PromoCodeBase(BaseModel):
    code: str
    discount: int
    active: bool = True
    max_uses: int = 100
    current_uses: int = 0
    expires_at: datetime | None = None
    discount_type: DiscountTypes = DiscountTypes.PERCENT


class PromoCodeCreate(PromoCodeBase):
    ...


class PromoCodeUpdate(PromoCodeCreate):
    ...


class PromoCodeUpdatePartial(PromoCodeUpdate):
    code: str | None = None
    discount: int | None = None
    active: bool | None = None
    max_uses: int | None = None
    current_uses: int | None = None
    discount_type: DiscountTypes | None = None


class PromoCodeSchema(PromoCodeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int