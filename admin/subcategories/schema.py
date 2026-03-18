from pydantic import BaseModel, ConfigDict


class SubCategories(BaseModel):
    title: str
    slug: str
    is_visible: bool

    category_title: str
    images: list[str]


class SubCategoriesForAdminList(SubCategories):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EditSubCategory(BaseModel):
    title: str | None = None
    slug: str | None = None
    is_visible: bool | None = None
    category_title: str | None = None
    images: list[str] | None = None