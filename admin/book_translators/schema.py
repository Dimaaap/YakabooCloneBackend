from pydantic import BaseModel, ConfigDict


class BookTranslators(BaseModel):
    first_name: str
    last_name: str
    slug: str
    is_active: bool



class BookTranslatorsListForAdminPage(BookTranslators):
    model_config = ConfigDict(from_attributes=True)

    id: int