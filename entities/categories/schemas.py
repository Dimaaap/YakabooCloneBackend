from pydantic import BaseModel, ConfigDict

from ..book_subcategory_banners.schema import BookSubcategoryBannerSchema
from ..book_subcategories.schema import BookSubcategorySchema


class CategoryBase(BaseModel):
    title: str
    slug: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryCreate):
    pass


class CategoryUpdatePartial(CategoryUpdate):
    title: str | None = None
    slug: str | None = None


class CategorySchema(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    banners: list[BookSubcategoryBannerSchema] = []
    subcategories: list[BookSubcategorySchema] = []
    id: int


class SubCategoryBase(BaseModel):
    title: str
    slug: str
    is_visible: bool = True
    category_id: int


class SubCategorySchema(SubCategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int