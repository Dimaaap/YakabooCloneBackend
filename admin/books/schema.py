from datetime import datetime

from pydantic import BaseModel, ConfigDict, PositiveInt


class Books(BaseModel):
    title: str
    slug: str
    price: PositiveInt = 0
    is_top: bool = False
    is_promo: bool = False
    is_in_chart: bool = False
    stars: int = 0
    promo_price: PositiveInt | None = None

    created_date: datetime | None = None
    is_notebook: bool = False

    book_info_id: int
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
