from pydantic import BaseModel, ConfigDict

from hobby_subcategories.schema import HobbySubcategorySchema


class HobbyCategoryBase(BaseModel):
    title: str
    slug: str
    images_src: list[str] | None = None


class HobbyCategoryCreate(HobbyCategoryBase):
    ...


class HobbyCategoryUpdate(HobbyCategoryCreate):
    ...


class HobbyCategoryUpdatePartial(HobbyCategoryUpdate):
    title: str | None = None
    slug: str | None = None


class HobbyCategorySchema(HobbyCategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    hobby_subcategories: list[HobbySubcategorySchema] = []


class HobbyCategoryShortSchema(HobbyCategoryBase):
    model_config = ConfigDict(from_attributes = True)

    id: int
