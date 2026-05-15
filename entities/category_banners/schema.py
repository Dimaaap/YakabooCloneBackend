from pydantic import BaseModel, ConfigDict


class CategoryBannerBase(BaseModel):
    image_url: str
    link: str


class CategoryBannerCreate(CategoryBannerBase):
    category_id: int


class CategoryBannerUpdatePartial(CategoryBannerCreate):
    image_url: str | None = None
    link: str | None = None
    category_id: int | None = None


class CategoryBannerSchema(CategoryBannerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int