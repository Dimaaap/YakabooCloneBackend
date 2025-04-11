from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .promo_category_association import PromoCategoryAssociation
    from .promotions import Promotion


class PromoCategories(Base):
    __tablename__ = "promo_categories"

    title: Mapped[str] = mapped_column(String(100), unique=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    promotions: Mapped[list["Promotion"]] = relationship(
        secondary="promo_category_association",
        back_populates="categories",
        overlaps="category_details"
    )

    promotion_details: Mapped[list["PromoCategoryAssociation"]] = relationship(
        back_populates="category",
        overlaps="categories,promotion"
    )

    def __str__(self):
        return f"{self.__class__.__name__} (title={self.title})"