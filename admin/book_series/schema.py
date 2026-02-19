from pydantic import BaseModel, ConfigDict


class BookSeriesList(BaseModel):
    title: str
    slug: str
    is_active: bool


class BookSeriesForAdminList(BookSeriesList):
    model_config = ConfigDict(from_attributes=True)

    id: int