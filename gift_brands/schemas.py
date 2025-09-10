from pydantic import BaseModel, ConfigDict


class GiftBrandBase(BaseModel):
    title: str
    slug: str
    image: str | None = None
    description: str | None = None
    visible: bool = True
    gifts: list[int] = []


class GiftBrandCreate(GiftBrandBase):
    ...


class GiftBrandUpdate(GiftBrandCreate):
    ...


class GiftBrandUpdatePartial(GiftBrandUpdate):
    title: str | None = None
    slug: str | None = None
    visible: bool | None = None
    gifts: list[int] | None = None


class GiftBrandSchema(GiftBrandBase):
    model_config = ConfigDict(from_attributes=True)

    id: int