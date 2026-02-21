from pydantic import BaseModel, ConfigDict


class Interesting(BaseModel):
    title: str
    slug: str
    visible: bool = True
    link: str


class InterestingForAdminList(Interesting):
    model_config = ConfigDict(from_attributes=True)

    id: int