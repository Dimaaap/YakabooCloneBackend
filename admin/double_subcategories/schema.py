from pydantic import BaseModel, ConfigDict


class DoubleSubCategories(BaseModel):
    title: str
    slug: str
    is_visible: bool

    subcategory_title: str
    images: list[str]


class DoubleSubcategoriesForAdminList(DoubleSubCategories):
    model_config = ConfigDict(from_attributes=True)

    id: int