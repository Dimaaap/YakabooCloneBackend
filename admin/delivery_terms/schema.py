from pydantic import BaseModel, ConfigDict


class CommonFieldsMixin:
    yakaboo_shop_price: int | None = None
    new_post_office_price: int | None = None
    new_post_department_price: int | None = None
    new_post_courier_price: int | None = None
    meest_post_price: int | None = None
    ukrpost_department_price: int | None = None
    ukrpost_courier_price: int | None = None


class DeliveryTerms(BaseModel, CommonFieldsMixin):
    country_title: str | None = None
    city_title: str | None = None


class DeliveryTermsForAdminList(DeliveryTerms):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EditDeliveryTerm(DeliveryTerms):
    ...


class CreateDeliveryTerm(BaseModel, CommonFieldsMixin):
    country_id: int | None = None
    city_id: int | None = None