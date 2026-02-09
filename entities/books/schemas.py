from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, conint
from fastapi import Query

from ..book_edition_group.schemas import BookEditionGroupSchema
from entities.book_illustrators.schemas import BookIllustratorSchema
from entities.book_info.schemas import BookInfoSchema
from ..authors.schemas import AuthorSchema
from entities.book_series.schema import BookSeriaSchema
from core.models.book_image import BookImageType
from ..notebook_subcategories.schemas import NotebookSubcategoryShortSchema
from entities.publishing.schemas import PublishingSchema
from entities.reviews.schema import ReviewSchema
from entities.wishlists.schemas import WishlistSchema
from ..notebook_categories.schema import NotebookCategoryShortSchema
from entities.book_translators.schemas import BookTranslatorSchema
from entities.literature_periods.schemas import LiteraturePeriodSchema



class BookImageSchema(BaseModel):
    image_url: str
    type: BookImageType

    model_config = ConfigDict(from_attributes=True)


class BookImageCreate(BookImageSchema):
    type: BookImageType = BookImageType.COVER


class BookBase(BaseModel):
    title: str = ""
    slug: str = ""
    price: int = 0
    is_top: bool = False
    is_promo: bool = False
    is_in_chart: bool = False
    is_notebook: bool = False
    stars: int = 0
    promo_price: int | None = None
    book_info_id: int | None = None
    notebook_category_id: int | None = None
    notebook_subcategory_id: int | None = None
    publishing_id: int
    edition_group_id: int | None = None
    seria_id: int | None = None
    images: list[BookImageCreate] | None = None
    authors: list[int] | None = None
    translators: list[int] | None = None
    created_date: datetime | None = None



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
    is_notebook: bool | None = None
    stars: int | None
    publishing_id: int | None


class BookSchemaWithoutWishlists(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_info: BookInfoSchema | None = None
    authors: list[AuthorSchema] = []
    publishing: PublishingSchema | None = None
    images: list[BookImageSchema] = []
    translators: list[BookTranslatorSchema] = []
    illustrators: list[BookIllustratorSchema] = []
    reviews: list[ReviewSchema] = []
    literature_period: LiteraturePeriodSchema | None = None
    notebook_category: NotebookCategoryShortSchema | None = None
    notebook_subcategory: NotebookSubcategoryShortSchema | None = None
    seria: BookSeriaSchema | None = None
    edition_group: BookEditionGroupSchema | None = None

class BookSchema(BookSchemaWithoutWishlists):
    wishlists: list[WishlistSchema] = []
    related_books: list["BookSchemaWithoutWishlists"] = Field(default_factory=list)


class PaginatedBookSchema(BaseModel):
    count: int
    limit: int
    offset: int
    has_more: bool
    results: list[BookSchema]


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