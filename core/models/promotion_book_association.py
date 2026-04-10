from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book import Book
    from .promotions import Promotion


class PromotionBookAssociation(Base):
    __tablename__ = "promotion_book_association"
    __table_args__ = (
        UniqueConstraint("book_id", "promotion_id", name="idx_unique_book_promo_pair"),
    )

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id")
    )
    promotion_id: Mapped[int] = mapped_column(ForeignKey("promotions.id"))

    book: Mapped["Book"] = relationship(
        back_populates="promotion_details"
    )
    promotion: Mapped["Promotion"] = relationship(
        back_populates="book_details"
    )