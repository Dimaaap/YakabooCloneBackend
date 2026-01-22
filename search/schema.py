from pydantic import BaseModel

from core.models.book_info import BookFormats


class BaseSearch(BaseModel):
    id: int


class SearchBook(BaseSearch):
    title: str
    slug: str
    code: int
    author_first_name: str | None
    author_last_name: str | None
    price: int
    image: str | None
    promo_price: int
    format: BookFormats


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


    