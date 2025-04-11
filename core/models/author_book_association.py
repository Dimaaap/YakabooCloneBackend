from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book import Book
    from .authors import Author


class AuthorBookAssociation(Base):
    __tablename__ = "author_book_association"
    __table_args__ = (
        UniqueConstraint("author_id", "book_id", name="idx_unique_author_book"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))

    author: Mapped["Author"] = relationship("Author",
                                            back_populates="author_details",
                                            overlaps="books,authors")
    book: Mapped["Book"] = relationship("Book",
                                        back_populates="author_details",
                                        overlaps="authors,books")

    def __str__(self):
        return f"{self.author.get_full_name}, {self.book.title}"