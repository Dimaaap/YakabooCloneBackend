from pydantic import BaseModel, ConfigDict

from core.models.book_info import CoverTypes, BookFormats, BookLanguages, PagesType, SizeTypes, PageFormats, \
    LiteratureTypes, LiteratureProgramClasses


class BookInfoBase(BaseModel):
    in_stock: bool | None = None
    bonuses: int | None = None
    visible: bool | None = None
    code: int
    rate: float
    illustrations: str | None = None
    ISBN: str
    cover_type: CoverTypes | None = None
    pages_count: int | None = None
    is_has_cashback: bool | None = None
    literature_type: LiteratureTypes | None = None
    literature_program_class: LiteratureProgramClasses | None = None
    present_edition_and_sets: str | None = None
    is_has_winter_esupport: bool | None = None
    is_has_esupport: bool | None = None
    is_for_war: bool | None = None
    format: BookFormats | None = None
    language: BookLanguages | None = None
    publishing_year: int | None = None
    first_published_at: int | None = None
    description: str | None = None
    characteristics: str | None = None
    weight: int | None = None
    original_name: str | None = None
    color: str | None = None
    has_color_cut: bool | None = None
    papers: PagesType | None = None
    pages_format: PageFormats | None = None
    print: str | None = None
    size: SizeTypes | None = None
    pages_color: str | None = None
    type: str | None = None
    edition: int | None = None
    book_format: str | None = None
    waiting_from: str | None = None
    is_free_delivery: bool | None = None
    delivery_time: int | None = None
    uk_delivery_time: int | None = None


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