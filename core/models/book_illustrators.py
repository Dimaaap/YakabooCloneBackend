from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book import Book
    from .illustrator_book_association import IllustratorBookAssociation


class BookIllustrator(Base):
    __tablename__ = "book_illustrators"

    first_name: Mapped[str] = mapped_column(String(255), default="", server_default="")
    last_name: Mapped[str] = mapped_column(String(255), default="", server_default="")
    slug: Mapped[str] = mapped_column(String(255), unique=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    book: Mapped[list["Book"]] = relationship(
        secondary="illustrator_book_association",
        back_populates="illustrators",
    )

    illustrator_details: Mapped[list["IllustratorBookAssociation"]] = relationship()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.__class__.__name__} (name={self.get_full_name()})"
