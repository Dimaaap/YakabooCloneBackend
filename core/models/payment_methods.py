from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .countries import Country
    from .city import City


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    cart_or_scholar_pack: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")
    winter_e_support: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")
    e_book: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")
    upon_receipt: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")
    prepay: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")
    privat_bank_parts: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")
    monobank_parts: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")

    country: Mapped["Country"] = relationship(back_populates="payment_methods",
                                              uselist=False,
                                              foreign_keys="PaymentMethod.country_id")
    country_id: Mapped[int | None] = mapped_column(ForeignKey("countries.id"), nullable=False)

    city: Mapped["City"] = relationship(back_populates="payment_methods",
                                        uselist=False,
                                        foreign_keys="PaymentMethod.city_id")
    city_id: Mapped[int | None] = mapped_column(ForeignKey("cities.id"), nullable=True)