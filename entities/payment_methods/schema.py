from pydantic import BaseModel, ConfigDict


class PaymentMethodBase(BaseModel):
    cart_or_scholar_pack: bool | None = None
    winter_e_support: bool | None = None
    e_book: bool | None = None
    privat_bank_parts: bool | None = None
    monobank_parts: bool | None = None
    upon_receipt: bool | None = None
    prepay: bool | None = None

    country_id: int | None = None
    city_id: int | None = None


class PaymentMethodCreate(PaymentMethodBase):
    pass


class PaymentMethodUpdate(PaymentMethodCreate):
    pass


class PaymentMethodUpdatePartial(PaymentMethodUpdate):
    pass


class PaymentMethodSchema(PaymentMethodBase):
    model_config = ConfigDict(from_attributes=True)

    id: int