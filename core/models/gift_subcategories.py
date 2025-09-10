from typing import TYPE_CHECKING

from sqlalchemy import String, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .gift_categories import GiftCategory
    from .gifts import Gift


class GiftSubCategory(Base):
    __tablename__ = 'gift_subcategories'

    title: Mapped[str] = mapped_column(String(50))
    slug: Mapped[str] = mapped_column(String(55), unique=True)
    images_src: Mapped[list[str]] = mapped_column(JSON, nullable=True)

    category_id: Mapped[int] = mapped_column(ForeignKey('gift_categories.id'))
    category: Mapped["GiftCategory"] = relationship("GiftCategory", back_populates="subcategories")

    gifts: Mapped[list["Gift"]] = relationship(
        "Gift",
        back_populates="gift_subcategory",
        cascade="all, delete-orphan"
    )

    def __str__(self):
        return f"{self.__class__.__name__} (title={self.title}, slug={self.slug})"