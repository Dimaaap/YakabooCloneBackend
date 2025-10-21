from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .subcategories import Subcategory
    from .subcategory_banners import SubcategoryBanner


class Category(Base):
    __tablename__ = "categories"

    title: Mapped[str] = mapped_column(String(100), unique=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True)

    subcategories: Mapped[list["Subcategory"]] = relationship("Subcategory", back_populates="category")
    banners: Mapped[list["SubcategoryBanner"]] = relationship(back_populates="category",
                                                              cascade="all, delete-orphan",
                                                              lazy="selectin")

    def __str__(self):
        return f"{self.__class__.__name__}(title={self.title})"

