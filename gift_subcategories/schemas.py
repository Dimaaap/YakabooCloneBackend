from pydantic import BaseModel, ConfigDict


class GiftSubcategoryBase(BaseModel):
    title: str
    slug: str
    images_src: list[dict[str, str]] | None = None
    category_id: int


class GiftSubcategoryCreate(GiftSubcategoryBase):
    ...


class GiftSubcategoryUpdate(GiftSubcategoryCreate):
    ...


class GiftSubcategoryUpdatePartial(GiftSubcategoryUpdate):
    title: str | None = None
    slug: str | None = None
    category_id: int | None = None


class GiftSubcategorySchema(GiftSubcategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class GiftSubcategoryShortSchema(GiftSubcategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int