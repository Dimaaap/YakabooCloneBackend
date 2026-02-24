from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from core.models.promo_code import DiscountTypes


class PromoCodes(BaseModel):
    code: str
    discount: int = Field(..., le=100)
    active: bool = True
    max_uses: int = 100
    current_uses: int = 0
    discount_type: DiscountTypes
    expires_at: datetime | None = None


class PromoCodesAdminList(PromoCodes):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: int