from pydantic import BaseModel, ConfigDict


class BookSeriesList(BaseModel):
    title: str
    slug: str
    is_active: bool


class BookSeriesForAdminList(BookSeriesList):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EditBookSeria(BaseModel):
    title: str | None = None
    slug: str | None = None
    is_active: bool | None = None


class CreateBookSeria(BookSeriesList):
    ...