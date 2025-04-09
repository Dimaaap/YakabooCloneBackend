from pydantic import BaseModel, ConfigDict


class WishlistBase(BaseModel):
    title: str
    is_active: bool | None = True


class WishlistUpdate(WishlistBase):
    pass


class WishlistCreate(WishlistBase):
    email: str


class WishlistUpdatePartial(WishlistUpdate):
    title: str | None


class WishlistSchema(WishlistBase):
    model_config = ConfigDict(from_attributes=True)

    id: int