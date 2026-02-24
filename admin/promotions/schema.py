from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Promotions(BaseModel):
    title: str
    slug: str
    image: str | None = None
    main_description: str
    short_description: str | None = None
    long_description: str | None = None
    end_date: datetime | None = None
    is_active: bool | None = None

    categories_title: list[str]


class PromotionsForAdminPage(Promotions):
    model_config = ConfigDict(from_attributes=True)

    id: int