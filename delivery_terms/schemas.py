from pydantic import BaseModel, ConfigDict


class DeliveryTermBase(BaseModel):
    yakaboo_shop_price: int | None = None
    new_post_office_price: int | None = None
    new_post_department_price: int | None = None
    new_post_courier_price: int | None = None
    meest_post_price: int | None = None
    ukrpost_department_price: int | None = None
    ukrpost_courier_price: int | None = None

    country_id: int | None = None
    city_id: int | None = None


class DeliveryTermCreate(DeliveryTermBase):
    pass


class DeliveryTermUpdate(DeliveryTermCreate):
    pass


class DeliveryTermUpdatePartial(DeliveryTermUpdate):
    pass


class DeliveryTermSchema(DeliveryTermBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
