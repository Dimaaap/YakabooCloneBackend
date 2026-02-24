from pydantic import BaseModel, ConfigDict


class PaymentMethods(BaseModel):
    cart_or_scholar_pack: bool = False
    winter_e_support: bool = False
    e_book: bool = False
    upon_receipt: bool = False
    prepay: bool = False
    privat_bank_parts: bool = False
    monobank_parts: bool = False

    country_title: str | None = None
    city_title: str | None = None


class PaymentMethodsForAdmin(PaymentMethods):
    model_config = ConfigDict(from_attributes=True)

    id: int