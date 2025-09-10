from pydantic import BaseModel, ConfigDict

from gift_subcategories.schemas import GiftSubcategorySchema


class GiftCategoryBase(BaseModel):
    title: str
    slug: str
    images_src: list[str] | None = None


class GiftCategoryCreate(GiftCategoryBase):
    ...


class GiftCategoryUpdate(GiftCategoryCreate):
    ...


class GiftCategoryUpdatePartial(GiftCategoryUpdate):
    title: str | None = None
    slug: str | None = None


class GiftCategorySchema(GiftCategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subcategories: list[GiftSubcategorySchema] = []


class GiftCategoryShortSchema(GiftCategoryBase):
    model_config = ConfigDict(from_attributes = True)

    id: int
