from pydantic import BaseModel, ConfigDict


class Publishing(BaseModel):
    title: str
    slug: str
    logo: str | None = None
    description: str | None = None
    visible: bool = True


class PublishingListForAdmin(Publishing):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EditPublishing(Publishing):
    title: str | None = None
    slug: str | None = None