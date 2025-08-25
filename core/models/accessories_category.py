from typing import TYPE_CHECKING

from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book_accessories import BookAccessories


class AccessoriesCategory(Base):
    __tablename__ = "accessories_categories"

    title: Mapped[str] = mapped_column(String(70))
    slug: Mapped[str] = mapped_column(String(70), unique=True)
    images_src: Mapped[list[str]] = mapped_column(JSON, nullable=True)

    accessories: Mapped[list["BookAccessories"]] = relationship("BookAccessories", back_populates="category",
                                                                cascade="all, delete-orphan")