from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book import Book
    from .categories import Category


class CategoryBookAssociation(Base):
    __tablename__ = "category_book_association"
    __table_args__ = (
        UniqueConstraint("book_id", "category_id", name="idx_unique_category_book"),
    )

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    category: Mapped["Category"] = relationship("Category",
                                                back_populates="category_details",
                                                overlaps="books")
    book: Mapped["Book"] = relationship("Book",
                                        back_populates="category_details",
                                        overlaps="categories")

