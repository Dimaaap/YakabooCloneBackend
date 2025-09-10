from typing import TYPE_CHECKING

from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .gifts import Gift
    from .gift_subcategories import GiftSubCategory


class GiftCategory(Base):
    __tablename__ = "gift_categories"

    title: Mapped[str] = mapped_column(String(50))
    slug: Mapped[str] = mapped_column(String(50), unique=True)
    images_src: Mapped[list[str]] = mapped_column(JSON, nullable=True)

    gifts: Mapped[list["Gift"]] = relationship("Gift", back_populates="gift_category",
                                                    cascade="all, delete-orphan")

    subcategories: Mapped[list["GiftSubCategory"]] = relationship(
        "GiftSubCategory",
        back_populates="category",
        cascade="all, delete-orphan"
    )


    def __str__(self) -> str:
        return f"{ self.__class__.__name__ }: (title={self.title}, slug={self.slug})"

