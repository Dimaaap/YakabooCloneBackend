from datetime import date

from pydantic import BaseModel, ConfigDict, field_validator



class AuthorsList(BaseModel):
    first_name: str
    last_name: str
    slug: str
    date_of_birth: date | None = None
    is_active: bool
    images_src: list[str] = []
    interesting_fact_text: str | None = None
    description: str | None = None
    short_description: str | None = None


class AuthorsListForAdmin(AuthorsList):
    model_config = ConfigDict(from_attributes=True)

    id: int


class AuthorsUpdate(AuthorsList):
    first_name: str | None = None
    last_name: str | None = None
    slug: str | None = None
    date_of_birth: date | None = None
    is_active: bool | None = None
    description: str | None = None

    @field_validator("date_of_birth", mode="before")
    def parse_empty_string(cls, v):
        if v == "":
            return None
        return v



class AuthorCreate(BaseModel):
    first_name: str
    last_name: str
    slug: str
    date_of_birth: str | None = None
    is_active: bool = True
    description: str | None = None
    images_src: list[str] = []