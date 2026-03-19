from pydantic import BaseModel, ConfigDict


class CommonFieldsMixin:
    title: str
    slug: str
    banner_images: list[str] = []


class Category(BaseModel, CommonFieldsMixin):
    subcategories_titles: list[str] = []


class CategoryForAdminList(Category):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EditCategory(BaseModel):
    title: str | None = None
    slug: str | None = None


class CreateCategory(BaseModel, CommonFieldsMixin):
    subcategories_ids: list[int] = []
