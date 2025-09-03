from typing import TYPE_CHECKING

from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book import Book
    from .notebook_subcategories import NotebookSubCategory


class NotebookCategory(Base):
    __tablename__ = "notebook_categories"

    title: Mapped[str] = mapped_column(String(50))
    slug: Mapped[str] = mapped_column(String(50), unique=True)
    images_src: Mapped[list[str]] = mapped_column(JSON, nullable=True)

    notebooks: Mapped[list["Book"]] = relationship("Book", back_populates="notebook_category",
                                                    cascade="all, delete-orphan")

    subcategories: Mapped[list["NotebookSubCategory"]] = relationship(
        "NotebookSubCategory",
        back_populates="category",
        cascade="all, delete-orphan"
    )


    def __str__(self) -> str:
        return f"{ self.__class__.__name__ }: (title={self.title}, slug={self.slug})"

