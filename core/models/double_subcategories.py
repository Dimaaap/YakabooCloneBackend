from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .subcategories import Subcategory
    from .book import Book
    from .double_subcategory_book_association import DoubleSubcategoryBookAssociation


class DoubleSubcategory(Base):
    __tablename__ = "double_subcategories"

    title: Mapped[str] = mapped_column(String(100), unique=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    subcategory_id: Mapped[int] = mapped_column(ForeignKey("sub_categories.id"))
    subcategory: Mapped["Subcategory"] = relationship("Subcategory", back_populates="double_subcategories")
    books: Mapped[list["Book"]] = relationship(
        secondary="double_subcategory_book_association",
        back_populates="double_subcategories"
    )

    book_details: Mapped[list["DoubleSubcategoryBookAssociation"]] = relationship(
        back_populates="double_subcategory",
        overlaps="books,double_subcategories",
    )

    images_src: Mapped[list[str]] = mapped_column(JSON, nullable=True)

    def __str__(self):
        return f"{ self.__class__.__name__ }(title={self.title}, slug={self.slug})"