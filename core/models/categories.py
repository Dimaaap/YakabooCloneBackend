from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .subcategories import Subcategory


class Category(Base):
    __tablename__ = "categories"

    title: Mapped[str] = mapped_column(String(100), unique=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True)

    subcategories: Mapped[list["Subcategory"]] = relationship("Subcategory", back_populates="category")

    def __str__(self):
        return f"{self.__class__.__name__}(title={self.title})"

