from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book import Book
    from .double_subcategories import DoubleSubcategory


class DoubleSubcategoryBookAssociation(Base):
    __tablename__ = "double_subcategory_book_association"
    __table_args__ = (
        UniqueConstraint("book_id", "double_subcategory_id",
                         name="idx_unique_double_subcategory_book"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    double_subcategory_id: Mapped[int] = mapped_column(ForeignKey("double_subcategories.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))

    double_subcategory: Mapped["DoubleSubcategory"] = relationship("DoubleSubcategory",
                                                                   back_populates="book_details",
                                                                   overlaps="books,double_subcategories")
    book: Mapped["Book"] = relationship("Book",
                                        back_populates="double_subcategories_details",
                                        overlaps="books,double_subcategories")