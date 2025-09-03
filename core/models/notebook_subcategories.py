from typing import TYPE_CHECKING

from sqlalchemy import String, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .notebook_categories import NotebookCategory
    from .book import Book


class NotebookSubCategory(Base):
    __tablename__ = 'notebook_subcategories'

    title: Mapped[str] = mapped_column(String(50))
    slug: Mapped[str] = mapped_column(String(55), unique=True)
    images_src: Mapped[list[str]] = mapped_column(JSON, nullable=True)

    category_id: Mapped[int] = mapped_column(ForeignKey('notebook_categories.id'))
    category: Mapped["NotebookCategory"] = relationship("NotebookCategory", back_populates="subcategories")

    notebooks: Mapped[list["Book"]] = relationship(
        "Book",
        back_populates="notebook_subcategory",
        cascade="all, delete-orphan"
    )

    def __str__(self):
        return f"{self.__class__.__name__} (title={self.title}, slug={self.slug})"