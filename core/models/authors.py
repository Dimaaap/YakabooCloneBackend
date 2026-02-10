from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import TSVECTOR

from .base import Base

if TYPE_CHECKING:
    from .author_images import AuthorImage
    from .book import Book
    from .author_book_association import AuthorBookAssociation
    from .author_facts import AuthorFacts


class Author(Base):
    first_name: Mapped[str] = mapped_column(String(255), default="", server_default="")
    last_name: Mapped[str] = mapped_column(String(255), default="", server_default="")
    slug: Mapped[str] = mapped_column(String(255), default="", server_default="")

    date_of_birth: Mapped[date] = mapped_column(Date, nullable=True, default=None)
    description: Mapped[str] = mapped_column(Text, default="", server_default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    short_description: Mapped[str] = mapped_column(Text, default="", server_default="")

    search_vector: Mapped[str] = mapped_column(TSVECTOR, nullable=True, default=None)

    images: Mapped[list["AuthorImage"]] = relationship("AuthorImage", back_populates="author", lazy="joined")

    book: Mapped[list["Book"]] = relationship(
        secondary="author_book_association",
        back_populates="authors"
    )

    author_details: Mapped[list["AuthorBookAssociation"]] = relationship(
        back_populates="author",
        overlaps="book"
    )

    interesting_fact: Mapped["AuthorFacts"] = relationship(
        "AuthorFacts",
        back_populates='author',
        lazy="joined",
        uselist=False
    )

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.__class__.__name__}(name={self.get_full_name()} slug={self.slug})"
