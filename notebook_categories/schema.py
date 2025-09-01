from pydantic import BaseModel, ConfigDict


class NotebookCategoryBase(BaseModel):
    title: str
    slug: str
    images_src: list[str] | None = None


class NotebookCategoryCreate(NotebookCategoryBase):
    ...


class NotebookCategoryUpdate(NotebookCategoryCreate):
    ...


class NotebookCategoryUpdatePartial(NotebookCategoryUpdate):
    title: str | None = None
    slug: str | None = None


class NotebookCategorySchema(NotebookCategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class NotebookCategoryShortSchema(NotebookCategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
