from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PromoCodeUsages(BaseModel):
    user_email: str
    promo_code_title: str

    used_at: datetime | None = None


class PromoCodeUsagesForAdmin(PromoCodeUsages):
    model_config = ConfigDict(from_attributes=True)

    id: int