from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .categories import Category


class SubcategoryBanner(Base):
    __tablename__ = "category_banners"

    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    link: Mapped[str] = mapped_column(String(250), nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"),
                                                nullable=False)
    category: Mapped["Category"] = relationship(back_populates="banners")