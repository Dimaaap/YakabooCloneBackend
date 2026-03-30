from pydantic import BaseModel, ConfigDict, conint


class DoubleSubcategoryBase(BaseModel):
    title: str
    slug: str
    is_visible: bool = True
    subcategory_id: int


class DoubleSubcategoryCreate(DoubleSubcategoryBase):
    images_src: list[str] | None = None


class DoubleSubcategoryUpdate(DoubleSubcategoryCreate):
    ...


class DoubleSubcategoryUpdatePartial(DoubleSubcategoryUpdate):
    title: str | None = None
    slug: str | None = None
    subcategory_id: int | None = None


class DoubleSubcategorySchema(DoubleSubcategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int