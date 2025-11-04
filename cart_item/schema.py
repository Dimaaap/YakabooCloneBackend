from pydantic import BaseModel, ConfigDict

from books.schemas import BookSchemaWithoutWishlists


class CartItemBase(BaseModel):
    quantity: int
    price: int
    cart_id: int
    book_id: int


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(CartItemCreate):
    pass


class CartItemUpdatePartial(CartItemUpdate):
    quantity: int | None = None
    price: int | None = None
    cart_id: int | None = None
    book_id: int | None = None


class CartItemSchema(CartItemBase):
    model_config = ConfigDict(from_attributes=True)

    book: BookSchemaWithoutWishlists | None = None
    id: int