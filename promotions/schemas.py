from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PromotionBase(BaseModel):
    title: str
    slug: str
    image: str | None = None
    main_description: str | None = None
    short_description: str | None = None
    long_description: str | None = None
    end_date: datetime | None = None
    is_active: bool = True


class PromotionCreate(PromotionBase):
    category_ids: list[int] = []


class PromotionUpdate(PromotionCreate):
    pass


class PromotionUpdatePartial(PromotionUpdate):
    title: str | None = None
    slug: str | None = None
    is_active: str | None = None


class PromotionSchema(PromotionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int