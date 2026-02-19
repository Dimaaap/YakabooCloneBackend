from pydantic import BaseModel, ConfigDict


class BookIllustratorsList(BaseModel):
    first_name: str
    last_name: str
    slug: str
    is_active: bool


class BookIllustratorsListForAdmin(BookIllustratorsList):
    model_config = ConfigDict(from_attributes=True)

    id: int