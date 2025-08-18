from pydantic import BaseModel, ConfigDict

from core.models.hobby import HobbyTheme, HobbyType
from core.models.board_game_ages import Age
from game_ages.schemas import GameAgeSchema, GameAgeHobbyCreate
from hobby_brand.schemas import HobbyBrandSchema
from hobby_categories.schemas import HobbyCategoryShortSchema
from hobby_subcategories.schema import HobbySubcategoryShortSchema


class HobbyImageSchema(BaseModel):
    image_url: str

    model_config = ConfigDict(from_attributes=True)


class HobbyImageCreate(HobbyImageSchema):
    ...


class HobbyGameSeriaSchema(BaseModel):
    title: str
    slug: str

    model_config = ConfigDict(from_attributes=True)


class HobbyBase(BaseModel):
    title: str
    slug: str
    description: str | None = None
    price: int
    image: str | None = None
    article: str
    size: str | None = None
    is_in_stock: bool
    bonuses: int
    weight: int | None = None
    code: int
    theme: HobbyTheme | None = None
    difficulty_level: int | None = None
    details_count: int | None = None
    packing: str | None = None
    color: str | None = None
    type: HobbyType | None = None
    ages: list[Age] = []
    brand_id: int
    seria_id: int | None = None
    images: list[HobbyImageCreate] | None = None
    category_id: int
    subcategory_id: int | None = None


class HobbyCreate(HobbyBase):
    ages: list[int] = []


class HobbyUpdate(HobbyCreate):
    ...


class HobbyUpdatePartial(HobbyUpdate):
    title: str | None = None
    slug: str | None = None
    price: int | None = None
    article: str | None = None
    code: int | None = None
    theme: HobbyTheme | None = None
    ages: list[GameAgeHobbyCreate] | None = None
    brand_id: int | None = None
    images: list[HobbyImageCreate] | None = None
    category_id: int | None = None
    is_in_stock: bool | None = None
    bonuses: int | None = None


class HobbySchema(HobbyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    images: list[HobbyImageSchema] = []
    ages: list[GameAgeSchema] = []
    brand: HobbyBrandSchema | None = None
    seria: HobbyGameSeriaSchema | None = None
    category: HobbyCategoryShortSchema | None = None
    subcategory: HobbySubcategoryShortSchema | None = None


class HobbyCountsResponse(BaseModel):
    total: int
    items: list[HobbySchema]
