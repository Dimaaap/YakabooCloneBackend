from pydantic import BaseModel, ConfigDict

from core.models.board_game_ages import Age
from game_ages.schemas import GameAgeSchema, GameAgeHobbyCreate
from gift_brands.schemas import GiftBrandSchema
from gift_categories.schemas import GiftCategoryShortSchema
from gift_subcategories.schemas import GiftSubcategoryShortSchema
from gift_series.schemas import GiftSeriaShortSchema


class GiftImageSchema(BaseModel):
    image_url: str

    model_config = ConfigDict(from_attributes=True)


class GiftImageCreate(GiftImageSchema):
    ...


class GiftBase(BaseModel):
    title: str
    slug: str
    price: int
    is_top: bool = False
    is_in_chart: bool = False
    gift_info_id: int
    seria_id: int | None = None
    gift_category_id: int | None = None
    gift_subcategory_id: int | None = None
    ages: list[Age] = []
    images: list[GiftImageCreate] | None = None


class GiftCreate(GiftBase):
    ...


class GiftUpdate(GiftCreate):
    ...


class GiftUpdatePartial(GiftUpdate):
    title: str | None = None
    slug: str | None = None
    price: int | None = None
    gift_info_id: int | None = None
    ages: list[Age] | None = None


class GiftSchema(GiftBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image: list[GiftImageSchema] = []
    ages: list[GameAgeSchema] = []
    brand: GiftBrandSchema | None = None
    seria: GiftSeriaShortSchema | None = None
    gift_category: GiftCategoryShortSchema | None = None
    gift_subcategory: GiftSubcategoryShortSchema | None = None

