from pydantic import BaseModel, ConfigDict


class Interesting(BaseModel):
    title: str
    slug: str
    visible: bool = True
    link: str


class InterestingForAdminList(Interesting):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EditInteresting(Interesting):
    title: str | None = None
    slug: str | None = None
    visible: bool | None = None
    link: str | None = None


class CreateInteresting(EditInteresting):
    ...