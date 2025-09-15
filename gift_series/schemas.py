from pydantic import BaseModel, ConfigDict


class GiftSeriaBase(BaseModel):
    title: str
    slug: str
    #gifts: list[int] | None = None


class GiftSeriaCreate(GiftSeriaBase):
    ...


class GiftSeriaUpdate(GiftSeriaCreate):
    ...


class GiftSeriaUpdatePartial(GiftSeriaUpdate):
    title: str | None = None
    slug: str | None = None


class GiftSeriaSchema(GiftSeriaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class GiftSeriaShortSchema(GiftSeriaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
