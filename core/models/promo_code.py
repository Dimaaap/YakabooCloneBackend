from typing import TYPE_CHECKING
from datetime import datetime
import enum

from sqlalchemy import String, Boolean, Integer, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .promo_code_usage import PromoCodeUsage


class DiscountTypes(str, enum.Enum):
    PERCENT = "percent"
    FIXED = "fixed"


class PromoCode(Base):
    __tablename__ = "promo_codes"

    code: Mapped[str] = mapped_column(String(50))
    discount: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    max_uses: Mapped[int] = mapped_column(Integer, default=100, server_default="100")
    current_uses: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    discount_type: Mapped[DiscountTypes] = mapped_column(SQLEnum(DiscountTypes,
                                                                 name="discount_type", create_type=True),
                                                         default=DiscountTypes.PERCENT,
                                                         server_default=DiscountTypes.PERCENT.name)

    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    usages: Mapped["PromoCodeUsage"] = relationship("PromoCodeUsage", back_populates="promo_code")

    def __str__(self):
        return f"{self.__class__.__name__} (code={self.code}, discount={self.discount})"
