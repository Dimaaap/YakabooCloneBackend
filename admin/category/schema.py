from pydantic import BaseModel, ConfigDict


class Category(BaseModel):
    title: str
    slug: str
    subcategories_titles: list[str] = []
    banner_images: list[str] = []


class CategoryForAdminList(Category):
    model_config = ConfigDict(from_attributes=True)

    id: int