from pydantic import BaseModel, ConfigDict


class HobbySubcategoryBase(BaseModel):
    title: str
    slug: str
    images_src: list[str] | None = None
    category_id: int


class HobbySubcategoryCreate(HobbySubcategoryBase):
    ...


class HobbySubcategoryUpdate(HobbySubcategoryCreate):
    ...


class HobbySubcategoryUpdatePartial(HobbySubcategoryUpdate):
    title: str | None = None
    slug: str | None = None


class HobbySubcategorySchema(HobbySubcategoryBase):
    model_config = ConfigDict(from_attributes = True)

    id: int


class HobbySubcategoryShortSchema(HobbySubcategoryBase):
    model_config = ConfigDict(from_attributes = True)

    id: int