from datetime import date

from pydantic import BaseModel, ConfigDict

from core.models import AuthorFacts


class AuthorsList(BaseModel):
    first_name: str
    last_name: str
    slug: str
    date_of_birth: date | None = None
    is_active: bool
    images_src: list[str] = []
    interesting_fact_text: str | None = None


class AuthorsListForAdmin(AuthorsList):
    model_config = ConfigDict(from_attributes=True)

    id: int


