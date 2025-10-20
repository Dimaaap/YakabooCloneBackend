from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book import Book


class BookEditionGroup(Base):
    __tablename__ = "book_edition_groups"

    title: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    books: Mapped[list["Book"]] = relationship("Book", back_populates="edition_group")

    def __str__(self) -> str:
        return f"{self.__class__.__name__} (title={self.title})"