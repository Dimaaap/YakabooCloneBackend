from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .gift_info import GiftInfo
    from .board_game_ages import BoardGameAge
    from .gift_brands import GiftBrand
    from .gift_series import GiftSeries
    from .gift_images import GiftImage
    from .gift_categories import GiftCategory
    from .gift_subcategories import GiftSubCategory


class Gift(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True)
    price: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    is_top: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    is_in_chart: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")

    gift_info_id: Mapped[int] = mapped_column(ForeignKey("gift_info.id", name="fk_gift_info"))
    gift_info: Mapped["GiftInfo"] = relationship("GiftInfo", back_populates="gift", lazy="joined")

    ages: Mapped[list["BoardGameAge"]] = relationship(
        secondary="gift_ages_association",
        back_populates="gifts",
    )

    brand_id: Mapped[int] = mapped_column(ForeignKey("gift_brands.id"))
    brand: Mapped["GiftBrand"] = relationship("GiftBrand", back_populates="gifts")

    seria_id: Mapped[int] = mapped_column(ForeignKey("gift_series.id"), nullable=True)
    seria: Mapped["GiftSeries"] = relationship("GiftSeries", back_populates="gifts")

    images: Mapped[list["GiftImage"]] = relationship(
        back_populates="gift",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    gift_category_id: Mapped[int] = mapped_column(
        ForeignKey("gift_categories.id", name="fk_gift_categories"),
        nullable=True
    )
    gift_category: Mapped["GiftCategory"] = relationship(
        "GiftCategory", back_populates="gifts", lazy="noload"
    )

    gift_subcategory_id: Mapped[int] = mapped_column(
        ForeignKey("gift_subcategories.id", name="fk_gift_subcategories"),
        nullable=True
    )

    gift_subcategory: Mapped["GiftSubCategory"] = relationship("GiftSubCategory",
                                                               back_populates="gifts")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(title={self.title}, slug={self.slug})"