from datetime import date

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    slug: str
    date_of_birth: date | None = None
    description: str | None = None
    is_active: bool = True


class AuthorCreate(AuthorBase):
    ...


class AuthorUpdate(AuthorCreate):
    ...


class AuthorSchema(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int