from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic_extra_types.phone_numbers import PhoneNumber

from core.models.order import DeliveryMethods, PaymentMethods, OrderStatus


class Orders(BaseModel):
    for_charity: bool = False
    other_person_get: bool = False
    delivery_method: DeliveryMethods
    getter_first_name: str | None = None
    getter_last_name: str | None = None
    getter_phone_number: PhoneNumber | None = None
    need_call: bool = True
    participant: bool = False
    have_questions: bool = False

    new_post_courier_delivery_address: str | None = None
    new_post_courier_delivery_apartment_number: int | None = None
    new_post_courier_house_number: int | None = None
    new_post_delivery_address: str | None = None
    ukrpost_courier_address: str | None = None
    ukrpost_courier_apartment_number: int | None = None
    ukrpost_courier_house_number: int | None = None
    ukrpost_user_first_name_for_courier: str | None = None
    ukrpost_user_middle_name_for_courier: str | None = None
    ukrpost_user_name_for_courier: str | None = None
    ukrpost_office_user_name: str | None = None
    ukrpost_office_user_middle_name: str | None = None
    ukrpost_office_user_last_name: str | None = None
    ukrpost_post_index: int | None = None

    payment_method: PaymentMethods
    comment: str | None = None
    create_date: datetime | None = None
    status: OrderStatus
    total_sum: int

    user_email: str
    city_title: str | None = None
    country_title: str | None = None
    new_post_number: int | None = None
    new_post_postomat: int | None = None
    ukrpost_office: int | None = None
    meest_post_office: int | None = None
    promo_usage: int | None = None


class OrdersForAdmin(Orders):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: int