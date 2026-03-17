from datetime import datetime

from pydantic import BaseModel, ConfigDict, PositiveInt


class BaseFieldsMixin:
    title: str
    slug: str
    price: PositiveInt = 0
    is_top: bool = False
    is_promo: bool = False
    is_in_chart: bool = False
    promo_price: PositiveInt | None = None

    created_date: datetime | None = None
    is_notebook: bool = False
    book_info_id: int


class Books(BaseModel, BaseFieldsMixin):
    authors_names: list[str] | None = None
    translators_names: list[str] | None = None
    illustrators_names: list[str] | None = None
    literature_period_title: str | None = None
    book_seria_title: str | None = None
    notebook_category_title: str | None = None
    notebook_subcategory_title: str | None = None
    subcategories_title: list[str] | None = None
    categories_title: list[str] | None = None
    double_subcategories_title: list[str] | None = None
    publishing_title: str | None = None
    edition_group_title: str | None = None
    book_images: list[str] | None = None


class BooksForAdminList(Books):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EditBook(Books):
    title: str | None = None
    slug: str | None = None
    price: PositiveInt | None = None
    book_info_id: int | None = None


class CreateBook(BaseModel, BaseFieldsMixin):
    author_ids: list[int]
    translators_ids: list[int] | None = None
    illustrators_ids: list[int] | None = None

    categories_ids: list[int] | None = None
    double_subcategories_ids: list[int] | None = None

    literature_period_id: int | None = None
    seria_id: int | None = None
    publishing_id: int
