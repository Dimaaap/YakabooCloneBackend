from enum import Enum

from pydantic import BaseModel, ConfigDict


class BookFormatsEnum(str, Enum):
    PAPER = "Паперова"
    ELECTRONIC = "Електронна"
    AUDIO = "Аудіо"


class BaseSearch(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SearchBook(BaseSearch):
    title: str
    slug: str
    code: int
    author_first_name: str | None
    author_last_name: str | None
    price: int
    image: str | None
    promo_price: int
    format: BookFormatsEnum


class SearchAuthors(BaseSearch):
    first_name: str
    last_name: str


class SearchPublishers(BaseSearch):
    title: str
    image_src: str | None


class SearchBookSeries(BaseSearch):
    title: str


class SearchResponse(BaseModel):
    books: list[SearchBook]
    authors: list[SearchAuthors]
    publishers: list[SearchPublishers]
    series: list[SearchBookSeries]


    