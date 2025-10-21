from pydantic import BaseModel, ConfigDict


class BookSubcategoryBase(BaseModel):
    title: str
    slug: str
    is_visible: bool = True
    category_id: int
    images_src: list[dict[str, str]] | None = None


class BookSubcategoryCreate(BookSubcategoryBase):
    ...


class BookSubcategoryUpdate(BookSubcategoryCreate):
    ...


class BookSubcategoryUpdatePartial(BookSubcategoryUpdate):
    title: str | None = None
    slug: str | None = None
    category_id: int | None = None


class BookSubcategorySchema(BookSubcategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
