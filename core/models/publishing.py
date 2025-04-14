from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book import Book


class Publishing(Base):
    title: Mapped[str] = mapped_column(String(200), unique=True)
    slug: Mapped[str] = mapped_column(String(200), unique=True)
    logo: Mapped[str] = mapped_column(String(255), default="", server_default="")
    short_description: Mapped[str] = mapped_column(Text, default="", server_default="")
    long_description: Mapped[str] = mapped_column(Text, default="", server_default="")
    visible: Mapped[bool] = mapped_column(Boolean, server_default="1", default=True)

    books: Mapped[list["Book"]] = relationship("Book",
                                               back_populates="publishing", cascade="all, delete-orphan")

    def __str__(self):
        return f"{self.__class__.__name__}(title={self.title}, slug={self.slug})"

