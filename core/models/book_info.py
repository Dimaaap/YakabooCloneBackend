import enum
from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, Enum, Integer, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book import Book
    
    
class BookFormats(enum.Enum):
    PAPER = "Паперова"
    ELECTRONIC = "Електронна"
    AUDIO = "Аудіо"


class BookLanguages(enum.Enum):
    UKRAINIAN = "Українська"
    ENGLISH = "Англійська"


class CoverTypes(enum.Enum):
    SOLID = "Тверда"
    SOFT = "М'яка"
    RINGS = "На кільцях"
    PAGE_PUBLISHING = "Листове видання"


class PagesType(enum.Enum):
    LINES = "Лінійка"
    CELL = "Клітинка"
    OBLIQUE = "Коса лінія"
    SIMPLE = "Прості"
    LAMINATED = "Ламіновані"


class SizeTypes(enum.Enum):
    SMALL = "Маленький",
    MEDIUM = "Середній",
    LARGE = "Великий"


class PageFormats(enum.Enum):
    A1 = "A1"
    A2 = "A2"
    A3 = "A3"
    A4 = "A4"
    A5 = "A5"


class LiteratureTypes(enum.Enum):
    FOREIGN = "Зарубіжна"
    UKRAINIAN = "Українська"


class LiteratureProgramClasses(enum.Enum):
    FIFTH = "5-й клас"
    SIXTH = "6-й клас"
    SEVENTH = "7-й клас"
    EIGHTH = "8-й клас"
    NINE = "9-й клас"
    TENTH = "10-й клас"
    ELEVENTH = "11-й клас"


class BookInfo(Base):
    __tablename__ = "book_info"

    in_stock: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    visible: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    code: Mapped[int] = mapped_column(Integer, unique=True)
    rate: Mapped[float] = mapped_column(Float, default=0, server_default="0")
    illustrations: Mapped[str] = mapped_column(String(255), default="", server_default="")
    ISBN: Mapped[str] = mapped_column(String(255), unique=True)
    cover_type: Mapped[CoverTypes] = mapped_column(Enum(CoverTypes), default=CoverTypes.SOLID,
                                                   server_default=CoverTypes.SOLID.name)
    pages_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    is_has_cashback: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    is_has_esupport: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    bonuses: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    literature_type: Mapped[LiteratureTypes] = mapped_column(Enum(LiteratureTypes,
                                                                  name="literature_type", create_type=True),
                                                             nullable=True)
    literature_program_class: Mapped[LiteratureProgramClasses] = mapped_column(Enum(LiteratureProgramClasses,
                                                                                    name="literature_program_class",
                                                                                    create_type=True),
                                                                               nullable=True)
    weight: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    original_name: Mapped[str] = mapped_column(String(255), default="", server_default="")

    format: Mapped[BookFormats] = mapped_column(Enum(BookFormats), default=BookFormats.PAPER,
                                                server_default=BookFormats.PAPER.name)
    pages_format: Mapped[PageFormats] = mapped_column(Enum(PageFormats, name="page_formats", create_type=True),
                                                      nullable=True)
    language: Mapped[BookLanguages] = mapped_column(Enum(BookLanguages), default=BookLanguages.UKRAINIAN,
                                                    server_default=BookLanguages.UKRAINIAN.name)
    color: Mapped[str] = mapped_column(String(100), nullable=True)
    papers: Mapped[PagesType] = mapped_column(Enum(PagesType), nullable=True)
    size: Mapped[SizeTypes] = mapped_column(Enum(SizeTypes), nullable=True)
    pages_color: Mapped[str] = mapped_column(String(50), nullable=True)
    type: Mapped[str] = mapped_column(String(50), nullable=True)
    edition: Mapped[int] = mapped_column(Integer, nullable=True)
    book_format: Mapped[str] = mapped_column(String(100), nullable=True)

    publishing_year: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    first_published_at: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    description: Mapped[str] = mapped_column(Text, default="", server_default="")
    characteristics: Mapped[str] = mapped_column(Text, default="", server_default="")

    book: Mapped["Book"] = relationship("Book", back_populates="book_info", uselist=False)

    def __str__(self):
        return f"{self.book.title}"
