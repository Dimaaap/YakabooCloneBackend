from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book import Book
    from .translator_book_association import TranslatorBookAssociation


class BookTranslator(Base):
    __tablename__ = 'book_translators'

    first_name: Mapped[str] = mapped_column(String(255), default="", server_default="")
    last_name: Mapped[str] = mapped_column(String(255), default="", server_default="")
    slug: Mapped[str] = mapped_column(String(255), unique=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    book: Mapped[list["Book"]] = relationship(
        secondary="translator_book_association",
        back_populates="translators",
    )

    translator_details: Mapped[list["TranslatorBookAssociation"]] = relationship(
        back_populates="translator",
        overlaps="books"
    )

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.__class__.__name__} (first name={self.first_name}, last name={self.last_name})"