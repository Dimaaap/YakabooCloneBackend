from pydantic import BaseModel, ConfigDict


class CommonFieldsMixin:
    title: str
    slug: str
    is_visible: bool


class DoubleSubCategories(BaseModel, CommonFieldsMixin):
    subcategory_title: str
    images: list[str] = []


class DoubleSubcategoriesForAdminList(DoubleSubCategories):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EditDoubleSubCategory(BaseModel):
    title: str | None = None
    slug: str | None = None
    is_visible: bool | None = None


class CreateDoubleSubCategory(BaseModel, CommonFieldsMixin):
    subcategory_id: int
    images_src: list[str] = []