from datetime import date

from pydantic import BaseModel, ConfigDict

from author_facts.schemas import AuthorFactSchema


class ImageBase(BaseModel):
    image_path: str = ""
    author_id: int


class ImageSchema(ImageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    slug: str
    date_of_birth: date | None = None
    description: str | None = None
    short_description: str | None = None
    is_active: bool = True
    interesting_fact: AuthorFactSchema | None = None
    images: list[ImageSchema] = []


class AuthorCreate(AuthorBase):
    ...


class AuthorUpdate(AuthorCreate):
    ...


class AuthorSchema(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int