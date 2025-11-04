from pydantic import BaseModel, ConfigDict

from cart_item.schema import CartItemSchema


class CartBase(BaseModel):
    user_id: int


class CartCreate(CartBase):
    pass


class CartUpdate(CartCreate):
    pass


class CartUpdatePartial(CartUpdate):
    pass


class CartSchema(CartBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    items: list[CartItemSchema] = []
