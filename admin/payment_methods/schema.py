from pydantic import BaseModel, ConfigDict, field_validator


class PaymentMethodsCommonFieldsMixin:
    cart_or_scholar_pack: bool = False
    winter_e_support: bool = False
    e_book: bool = False
    upon_receipt: bool = False
    prepay: bool = False
    privat_bank_parts: bool = False
    monobank_parts: bool = False


class PaymentMethods(BaseModel, PaymentMethodsCommonFieldsMixin):
    country_title: str | None = None
    city_title: str | None = None


class PaymentMethodsForAdmin(PaymentMethods):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EditPaymentMethod(PaymentMethods):
    ...


class CreatePaymentMethod(BaseModel, PaymentMethodsCommonFieldsMixin):
    country_id: int | None = None
    city_id: int | None = None

    @field_validator("country_id", "city_id", mode="before")
    @classmethod
    def convert_zero_to_none(cls, value):
        if value == 0:
            return None
        return value

