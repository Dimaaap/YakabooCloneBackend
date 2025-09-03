from pydantic import BaseModel, ConfigDict


class NotebookSubcategoryBase(BaseModel):
    title: str
    slug: str
    images_src: list[dict[str, str]] | None = None
    category_id: int


class NotebookSubcategoryCreate(NotebookSubcategoryBase):
    ...


class NotebookSubcategoryUpdate(NotebookSubcategoryCreate):
    ...


class NotebookSubcategoryUpdatePartial(NotebookSubcategoryUpdate):
    title: str | None = None
    slug: str | None = None
    category_id: int | None = None


class NotebookSubcategorySchema(NotebookSubcategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class NotebookSubcategoryShortSchema(NotebookSubcategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


