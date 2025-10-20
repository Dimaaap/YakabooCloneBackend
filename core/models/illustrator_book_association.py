from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book import Book
    from .book_illustrators import BookIllustrator


class IllustratorBookAssociation(Base):
    __tablename__ = "illustrator_book_association"
    __table_args__ = (
        UniqueConstraint("book_id", "illustrator_id", name="idx_unique_illustrator_book"),
    )

    illustrator_id: Mapped[int] = mapped_column(ForeignKey("book_illustrators.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))

    illustrator: Mapped["BookIllustrator"] = relationship("BookIllustrator",
                                                          back_populates="illustrator_details",
                                                          overlaps="books")
    book: Mapped["Book"] = relationship("Book",
                                        back_populates="illustrator_details",
                                        overlaps="translators")

    def __str__(self) -> str:
        return f"{self.illustrator.get_full_name()}"