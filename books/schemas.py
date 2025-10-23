from pydantic import BaseModel, ConfigDict, Field

from book_edition_group.schemas import BookEditionGroupSchema
from book_illustrators.schemas import BookIllustratorSchema
from book_info.schemas import BookInfoSchema
from authors.schemas import AuthorSchema
from book_series.schema import BookSeriaSchema
from core.models.book_image import BookImageType
from notebook_subcategories.schemas import NotebookSubcategoryShortSchema
from publishing.schemas import PublishingSchema
from wishlists.schemas import WishlistSchema
from notebook_categories.schema import NotebookCategoryShortSchema
from book_translators.schemas import BookTranslatorSchema
from literature_periods.schemas import LiteraturePeriodSchema



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
    literature_period: LiteraturePeriodSchema | None = None
    notebook_category: NotebookCategoryShortSchema | None = None
    notebook_subcategory: NotebookSubcategoryShortSchema | None = None
    seria: BookSeriaSchema | None = None
    edition_group: BookEditionGroupSchema | None = None

class BookSchema(BookSchemaWithoutWishlists):
    wishlists: list[WishlistSchema] = []
    related_books: list["BookSchemaWithoutWishlists"] = Field(default_factory=list)
