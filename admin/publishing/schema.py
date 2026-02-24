from pydantic import BaseModel, ConfigDict


class Publishing(BaseModel):
    title: str
    slug: str
    logo: str | None = None
    short_description: str | None = None
    long_description: str | None = None
    visible: bool = True


class PublishingListForAdmin(Publishing):
    model_config = ConfigDict(from_attributes=True)

    id: int