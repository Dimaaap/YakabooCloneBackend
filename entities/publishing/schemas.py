from pydantic import BaseModel, ConfigDict, conint


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

class BookFilters(BaseModel):
    limit: conint(ge=1, le=100) = 100
    offset: conint(ge=0) = 0
    categories: list[str] | None = None
    publishers: list[str] | None = None
    languages: list[str] | None = None
    bookTypes: list[str] | None = None
    authors: list[str] | None = None
    series: list[str] | None = None
    in_stock: bool | None = None
    price_min: int | None = None
    price_max: int | None = None
    filters: list[str] | None = None


