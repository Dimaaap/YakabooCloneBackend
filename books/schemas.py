from pydantic import BaseModel, ConfigDict

from book_info.schemas import BookInfoSchema
from authors.schemas import AuthorSchema
from core.models.book_image import BookImageType
from publishing.schemas import PublishingSchema
from wishlists.schemas import WishlistSchema


class BookImageSchema(BaseModel):
    image_url: str
    type: BookImageType


class BookImageCreate(BookImageSchema):
    type: BookImageType = BookImageType.COVER

class BookBase(BaseModel):
    title: str = ""
    slug: str = ""
    price: int = 0
    is_top: bool = False
    is_promo: bool = False
    is_in_chart: bool = False
    stars: int = 0
    promo_price: int | None = None
    book_info_id: int | None = None
    publishing_id: int
    images: list[BookImageCreate] | None = None


class BookCreate(BookBase):
    ...


class BookUpdate(BookCreate):
    ...


class BookUpdatePartial(BookUpdate):
    title: str | None = None
    slug: str | None = None
    price: int | None = None
    is_top: bool | None = None
    is_promo: bool | None = None
    is_in_chart: bool | None = None
    stars: int | None
    publishing_id: int | None


class BookSchema(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_info: BookInfoSchema | None = None
    authors: list[AuthorSchema] = []
    publishing: PublishingSchema | None = None
    wishlists: list[WishlistSchema] = []
    images: list[BookImageSchema] = []
