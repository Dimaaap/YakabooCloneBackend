from pydantic import BaseModel, ConfigDict


class BookIllustratorsList(BaseModel):
    first_name: str
    last_name: str
    slug: str
    is_active: bool


class BookIllustratorsListForAdmin(BookIllustratorsList):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EditBookIllustrator(BookIllustratorsList):
    first_name: str | None = None
    last_name: str | None = None
    slug: str | None = None
    is_active: bool | None = None