from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .promotions import Promotion
    from .promo_categories import PromoCategories


class PromoCategoryAssociation(Base):
    __tablename__ = "promo_category_association"
    __table_args__ = (
        UniqueConstraint("promotion_id", "category_id", name="idx_unique_promo_category"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("promo_categories.id"))
    promotion_id: Mapped[int] = mapped_column(ForeignKey("promotions.id"))

    category: Mapped["PromoCategories"] = relationship(
        back_populates="promotion_details",
        overlaps="categories,promotions"
    )

    promotion: Mapped["Promotion"] = relationship(
        back_populates="category_details",
        overlaps="categories,promotions"
    )


