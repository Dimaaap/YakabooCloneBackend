from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book import Book
    from .book_translators import BookTranslator


class TranslatorBookAssociation(Base):
    __tablename__ = "translator_book_association"
    __table_args__ = (
        UniqueConstraint("translator_id", "book_id", name="idx_unique_translator_book"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    translator_id: Mapped[int] = mapped_column(ForeignKey("book_translators.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))

    translator: Mapped["BookTranslator"] = relationship("BookTranslator",
                                                        back_populates="translator_details",
                                                        overlaps="books")
    book: Mapped["Book"] = relationship("Book",
                                        back_populates="translator_details",
                                        overlaps="translators")
    def __str__(self):
        return f"{self.translator.get_full_name()}"