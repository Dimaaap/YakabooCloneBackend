from typing import TYPE_CHECKING

from sqlalchemy import String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book_accessories import BookAccessories


class AccessoriesBrand(Base):
    __tablename__ = "accessories_brands"

    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255))
    image: Mapped[str] = mapped_column(Text, default="", server_default="", nullable=True)
    accessories: Mapped[list["BookAccessories"]] = relationship(
        "BookAccessories",
        back_populates="brand",
        cascade="all, delete-orphan",
    )

    def __str__(self) -> str:
        return f"{ self.__class__.__name__ } (id={self.id}, title={self.title} slug={self.slug})"