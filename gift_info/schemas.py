from pydantic import BaseModel, ConfigDict

from core.models.gift_info import GiftThemeEnum, GiftLanguagesEnum, GiftEventEnum, GiftTypeEnum


class GiftInfoBase(BaseModel):
    in_stock: bool = True
    visible: bool = True
    code: int
    rate: float | None = None
    ISBN: str
    bonuses: int | None = None
    is_has_esupport: bool = False
    is_has_cashback: bool = False
    pages_count: int | None = None
    item_size: str | None = None
    packing_size: str | None = None
    illustrations: str | None = None
    packing_type: str | None = None
    cover_type: str | None = None
    colors: str | None = None
    weight: int | None = None
    publishing_year: int | None = None
    description: str | None = None
    language: GiftLanguagesEnum | None = None
    gift_type: GiftTypeEnum | None = None
    theme: GiftThemeEnum | None = None
    event: GiftEventEnum | None = None


class GiftInfoCreate(GiftInfoBase):
    ...


class GiftInfoUpdate(GiftInfoCreate):
    ...


class GiftInfoUpdatePartial(GiftInfoUpdate):
    code: int | None = None
    ISBN: str | None = None


class GiftInfoSchema(GiftInfoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
