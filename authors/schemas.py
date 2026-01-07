from datetime import date

from pydantic import BaseModel, ConfigDict, conint

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


class BookFilters(BaseModel):
    limit: conint(ge=1, le=100) = 100
    offset: conint(ge=0) = 0
    categories: list[str] | None = None
    publishers: list[str] | None = None
    languages: list[str] | None = None
    bookTypes: list[str] | None = None
    authors: list[str] | None = None
    series: list[str] | None = None
    in_stock: bool | None = None
    price_min: int | None = None
    price_max: int | None = None
    filters: list[str] | None = None