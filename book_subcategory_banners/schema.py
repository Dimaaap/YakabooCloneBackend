from pydantic import BaseModel, ConfigDict


class BookSubcategoryBannerBase(BaseModel):
    image_url: str
    category_id: int
    link: str


class BookSubcategoryBannerCreate(BookSubcategoryBannerBase):
    ...


class BookSubcategoryBannerUpdate(BookSubcategoryBannerCreate):
    ...


class BookSubcategoryBannerUpdatePartial(BookSubcategoryBannerUpdate):
    image_url: str | None
    category_id: int | None = None
    link: str | None = None


class BookSubcategoryBannerSchema(BookSubcategoryBannerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

