from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book import Book
    from .subcategories import Subcategory


class SubcategoryBookAssociation(Base):
    __tablename__ = "subcategory_book_association"
    __table_args__ = (
        UniqueConstraint("book_id", "subcategory_id",
                         name="idx_unique_subcategory_book"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    subcategory_id: Mapped[int] = mapped_column(ForeignKey("sub_categories.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))

    subcategory: Mapped["Subcategory"] = relationship("Subcategory",
                                                      back_populates="book_details",
                                                      overlaps="books,subcategories")
    book: Mapped["Book"] = relationship("Book",
                                        back_populates="subcategoires_details")