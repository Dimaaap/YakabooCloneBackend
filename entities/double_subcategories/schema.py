from pydantic import BaseModel, ConfigDict


class DoubleSubcategoryBase(BaseModel):
    title: str
    slug: str
    is_visible: bool = True
    subcategory_id: int
    images_src: list[dict[str, str]] | None = None


class DoubleSubcategoryCreate(DoubleSubcategoryBase):
    ...


class DoubleSubcategoryUpdate(DoubleSubcategoryCreate):
    ...


class DoubleSubcategoryUpdatePartial(DoubleSubcategoryUpdate):
    title: str | None = None
    slug: str | None = None
    subcategory_id: int | None = None


class DoubleSubcategorySchema(DoubleSubcategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int