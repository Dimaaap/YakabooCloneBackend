from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book import Book


class BookSeria(Base):
    __tablename__ = 'book_series'

    title: Mapped[str] = mapped_column(String(150), unique=True)
    slug: Mapped[str] = mapped_column(String(150), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default='1')

    books: Mapped[list["Book"]] = relationship(
        "Book", back_populates="seria", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(title={self.title}, slug={self.slug})"

