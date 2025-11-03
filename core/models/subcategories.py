from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .categories import Category
    from .subcategory_book_association import SubcategoryBookAssociation
    from .double_subcategories import DoubleSubcategory
    from .book import Book


class Subcategory(Base):
    __tablename__ = "sub_categories"

    title: Mapped[str] = mapped_column(String(100), unique=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    category: Mapped["Category"] = relationship("Category", back_populates="subcategories")

    double_subcategories: Mapped[list["DoubleSubcategory"]] = relationship("DoubleSubcategory",
                                                                           back_populates="subcategory",
                                                                           lazy="selectin")
    books: Mapped[list["Book"]] = relationship(
        secondary="subcategory_book_association",
        back_populates="subcategories"
    )

    book_details: Mapped[list["SubcategoryBookAssociation"]] = relationship(
        back_populates="subcategory",
        overlaps="books"
    )
    images_src: Mapped[list[str]] = mapped_column(JSON, nullable=True)


    def __str__(self):
        return f"{self.__class__.__name__}(title={self.title})"