from pydantic import BaseModel, ConfigDict


class PublishingBase(BaseModel):
    title: str
    slug: str
    logo: str = ""
    short_description: str = ""
    long_description: str = ""
    visible: bool = True


class SearchQuery(BaseModel):
    q: str


class PublishingCreate(PublishingBase):
    pass


class PublishingUpdate(PublishingCreate):
    pass


class PublishingUpdatePartial(PublishingUpdate):
    title: str | None = None
    slug: str | None = None
    logo: str | None = None
    short_description: str | None = None
    long_description: str | None = None
    visible: bool | None = True


class PublishingSchema(PublishingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


