from pydantic import BaseModel, ConfigDict


class PublishingBannerBase(BaseModel):
    image_src: str
    publishing_id: int
    link: str | None = None


class PublishingBannerCreate(PublishingBannerBase):
    ...


class PublishingBannerUpdate(PublishingBannerCreate):
    ...


class PublishingBannerUpdatePartial(PublishingBannerUpdate):
    image_src: str | None = None
    publishing_id: int | None = None


class PublishingBannerSchema(PublishingBannerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


