from pydantic import BaseModel, ConfigDict


class BookTranslators(BaseModel):
    first_name: str
    last_name: str
    slug: str
    is_active: bool



class BookTranslatorsListForAdminPage(BookTranslators):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EditBookTranslator(BookTranslators):
    first_name: str | None = None
    last_name: str | None = None
    slug: str | None = None
    is_active: bool | None = None