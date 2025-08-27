from pydantic import BaseModel, ConfigDict

from accessories_brands.schemas import AccessoryBrandSchema
from accessories_categories.schemas import AccessoryCategorySchema
from core.models.book_accessories import Events, AccessoryTheme, AccessorySeria


class AccessoriesImageSchema(BaseModel):
    image_url: str

    model_config = ConfigDict(from_attributes=True)


class AccessoriesImageCreate(AccessoriesImageSchema):
    ...



class AccessoriesBase(BaseModel):
    title: str
    slug: str
    description: str | None = None
    price: int
    image: str | None = None
    article: str
    size: str | None = None
    code: int
    weight: float | None = None
    is_in_top: bool = False
    is_new: bool = False
    is_in_stock: bool = True
    bonuses: int = 0
    color: list[str] = []
    packing: str | None = None
    event: Events | None = None
    type: AccessoryTheme | None = None
    seria: AccessorySeria | None = None
    images: list[AccessoriesImageCreate] | None = None
    brand_id: int | None = None
    category_id: int | None = None


class AccessoriesCreate(AccessoriesBase):
    ...


class AccessoriesUpdate(AccessoriesCreate):
    ...


class AccessoriesUpdatePartial(AccessoriesUpdate):
    title: str | None = None
    slug: str | None = None
    price: int | None = None
    article: str | None = None
    code: str | None = None
    is_in_top: bool | None = None
    is_new: bool | None = None
    is_in_stock: bool | None = None
    bonuses: int | None = None
    color: list[str] | None = None


class AccessoriesSchema(AccessoriesBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    images: list[AccessoriesImageSchema] = []
    brand: AccessoryBrandSchema | None = None
    category: AccessoryCategorySchema | None = None