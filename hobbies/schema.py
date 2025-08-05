from pydantic import BaseModel, ConfigDict

from core.models.hobby import HobbyTheme
from game_ages.schemas import GameAgeSchema
from hobby_brand.schemas import HobbyBrandSchema
from hobby_categories.schemas import HobbyCategorySchema


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
    weight: int | None = None
    code: int
    theme: HobbyTheme
    difficulty_level: int | None = None
    details_count: int | None = None
    ages: list[GameAgeSchema] = []
    brand_id: int
    seria_id: int
    images: list[HobbyImageCreate] | None = None
    category_id: int


class HobbyCreate(HobbyBase):
    ...


class HobbyUpdate(HobbyCreate):
    ...


class HobbyUpdatePartial(HobbyUpdate):
    title: str | None = None
    slug: str | None = None
    price: int | None = None
    article: str | None = None
    code: int | None = None
    theme: HobbyTheme | None = None
    ages: list[GameAgeSchema] | None = None
    brand_id: int | None = None
    seria_id: int | None = None
    images: list[HobbyImageCreate] | None = None
    category_id: int | None = None


class HobbyShema(HobbyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    images: list[HobbyImageSchema] = []
    ages: list[GameAgeSchema]
    brand: HobbyBrandSchema | None = None
    seria: HobbyGameSeriaSchema | None = None
    category: HobbyCategorySchema | None = None


