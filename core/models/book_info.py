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


class PagesType(enum.Enum):
    LINES = "Лінійка"
    CELL = "Клітинка"
    OBLIQUE = "Коса лінія"
    SIMPLE = "Прості"


class SizeTypes(enum.Enum):
    SMALL = "Маленький",
    MEDIUM = "Середній",
    LARGE = "Великий"


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

    weight: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    original_name: Mapped[str] = mapped_column(String(255), default="", server_default="")

    format: Mapped[BookFormats] = mapped_column(Enum(BookFormats), default=BookFormats.PAPER,
                                                server_default=BookFormats.PAPER.name)
    language: Mapped[BookLanguages] = mapped_column(Enum(BookLanguages), default=BookLanguages.UKRAINIAN,
                                                    server_default=BookLanguages.UKRAINIAN.name)
    color: Mapped[str] = mapped_column(String(100), nullable=True)
    papers: Mapped[PagesType] = mapped_column(Enum(PagesType), nullable=True)
    size: Mapped[SizeTypes] = mapped_column(Enum(SizeTypes), nullable=True)
    pages_color: Mapped[str] = mapped_column(String(50), nullable=True)
    type: Mapped[str] = mapped_column(String(50), nullable=True)

    publishing_year: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    first_published_at: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    description: Mapped[str] = mapped_column(Text, default="", server_default="")
    characteristics: Mapped[str] = mapped_column(Text, default="", server_default="")

    book: Mapped["Book"] = relationship("Book", back_populates="book_info", uselist=False)

    def __str__(self):
        return f"{self.book.title}"
