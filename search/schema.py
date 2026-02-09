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
    author_first_name: str | None = None
    author_last_name: str | None = None
    price: int
    image: str | None = None
    promo_price: int | None = None
    format: BookFormatsEnum
    in_stock: bool
    stars: int
    comments_count: int | None = None
    is_top: bool = False
    is_new: bool = False
    is_promo: bool = False
    is_has_cashback: bool = False
    is_has_winter_esupport: bool = False
    is_has_esupport: bool = False
    uk_delivery_time: int | None = None
    delivery_time: int | None = None


class SearchAuthors(BaseSearch):
    first_name: str
    last_name: str
    slug: str
    image: str | None = None


class SearchPublishers(BaseSearch):
    title: str
    slug: str
    logo: str | None


class SearchBookSeries(BaseSearch):
    title: str
    slug: str


class SearchResponse(BaseModel):
    books: list[SearchBook]
    authors: list[SearchAuthors]
    publishers: list[SearchPublishers]
    series: list[SearchBookSeries]
    also_searched: list[str]


    