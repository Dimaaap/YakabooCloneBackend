from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .promo_categories import PromoCategories
    from .promo_category_association import PromoCategoryAssociation
    from .book import Book
    from .promotion_book_association import PromotionBookAssociation


class Promotion(Base):
    title: Mapped[str] = mapped_column(String(180), unique=True)
    slug: Mapped[str] = mapped_column(String(180), unique=True)

    image: Mapped[str] = mapped_column(String(200), default="", server_default="")
    main_description: Mapped[str] = mapped_column(Text, default="", server_default="")
    short_description: Mapped[str] = mapped_column(Text, default="", server_default="")
    long_description: Mapped[str] = mapped_column(Text, default="", server_default="")
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    categories: Mapped[list["PromoCategories"]] = relationship(
        secondary="promo_category_association",
        back_populates="promotions"
    )

    category_details: Mapped[list["PromoCategoryAssociation"]] = relationship(
        back_populates="promotion",
        overlaps="categories"
    )

    books: Mapped[list["Book"]] = relationship(
        "Book",
        secondary="promotion_book_association",
        back_populates="promotions"
    )

    book_details: Mapped[list["PromotionBookAssociation"]] = relationship(
        "PromotionBookAssociation",
        back_populates="promotion",
        cascade="all, delete-orphan",
    )

    def __str__(self):
        return f"{self.__class__.__name__}(title={self.title}, end_date={self.end_date})"