from pydantic import BaseModel, ConfigDict

from core.models.book_info import CoverTypes, LiteratureTypes, LiteratureProgramClasses, BookFormats, PageFormats, \
    BookLanguages, PagesType, SizeTypes


class BookInfo(BaseModel):
    in_stock: bool = True
    visible: bool = True
    code: int
    rate: float = 0
    illustrations: str | None = None
    ISBN: str
    cover_type: CoverTypes
    pages_count: int | None = None
    is_has_cashback: bool = False
    is_has_winter_esupport: bool = False
    is_has_esupport: bool = False
    is_for_war: bool = False
    bonuses: int = 0
    literature_type: LiteratureTypes | None = None
    literature_program_class: LiteratureProgramClasses | None = None
    present_edition_and_sets: str | None = None
    weight: int = 0
    original_name: str | None = None
    format: BookFormats | None = None
    pages_format: PageFormats | None = None
    language: BookLanguages | None = None
    color: str | None = None
    papers: PagesType | None = None
    size: SizeTypes | None = None
    pages_color: str | None = None
    type: str | None = None
    edition: int | None = None
    book_format: str | None = None
    waiting_from: str | None = None
    is_free_delivery: bool = False
    delivery_time: int | None = None
    uk_delivery_time: int | None = None
    has_color_cut: bool = False
    print: str | None = None
    publishing_year: int | None = None
    first_published_at: int | None = None
    description: str = ""
    characteristics: str | None = None

    book_title: str


class BookInfoListForAdmin(BookInfo):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: int

