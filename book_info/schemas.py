from pydantic import BaseModel, ConfigDict

from core.models.book_info import CoverTypes, BookFormats, BookLanguages


class BookInfoBase(BaseModel):
    in_stock: bool | None = None
    bonuses: int | None = None
    visible: bool | None = None
    code: int
    rate: float
    illustrations: str | None = None
    ISBN: str
    cover_type: CoverTypes
    pages_count: int | None = None
    is_has_cashback: bool | None = None
    is_has_esupport: bool | None = None
    format: BookFormats
    language: BookLanguages
    publishing_year: int
    first_published_at: int | None = None
    description: str | None = None
    characteristics: str | None = None
    weight: int | None = None
    original_name: str | None = None


class BookInfoCreate(BookInfoBase):
    ...


class BookInfoUpdate(BookInfoCreate):
    ...


class BookInfoUpdatePartial(BookInfoUpdate):
    code: int | None = None
    rate: float | None = None
    ISBN: str | None = None
    cover_type: CoverTypes | None = None
    format: BookFormats | None = None
    language: BookLanguages | None = None
    publishing_year: int | None = None


class BookInfoSchema(BookInfoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int