from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base

if TYPE_CHECKING:
    from .promo_code import PromoCode
    from .user import User
    from .order import Order


class PromoCodeUsage(Base):
    __tablename__ = "promo_code_usages"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    promo_id: Mapped[int] = mapped_column(ForeignKey("promo_codes.id", ondelete="CASCADE"))
    used_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), server_default=str(datetime.now()))

    user: Mapped["User"] = relationship("User", back_populates="promo_usage")
    promo_code: Mapped["PromoCode"] = relationship("PromoCode", back_populates="usages")

    order: Mapped["Order"] = relationship("Order", back_populates="promo_usage", uselist=False)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(user_id={self.user_id}, promo_id={self.promo_id})"
