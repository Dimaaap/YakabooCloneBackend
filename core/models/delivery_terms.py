from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .countries import Country
    from .city import City


class DeliveryTerms(Base):
    __tablename__ = "delivery_terms"

    yakaboo_shop_price: Mapped[int] = mapped_column(Integer, nullable=True)
    new_post_office_price: Mapped[int] = mapped_column(Integer, nullable=True)
    new_post_department_price: Mapped[int] = mapped_column(Integer, nullable=True)
    new_post_courier_price: Mapped[int] = mapped_column(Integer, nullable=True)
    meest_post_price: Mapped[int] = mapped_column(Integer, nullable=True)
    ukrpost_department_price: Mapped[int] = mapped_column(Integer, nullable=True)
    ukrpost_courier_price: Mapped[int] = mapped_column(Integer, nullable=True)

    country: Mapped["Country"] = relationship(back_populates="delivery_terms",
                                              uselist=False,
                                              foreign_keys="DeliveryTerms.country_id")
    country_id: Mapped[int | None] = mapped_column(ForeignKey("countries.id"), nullable=True)
    city: Mapped["City"] = relationship(back_populates="delivery_terms",
                                        uselist=False,
                                        foreign_keys="DeliveryTerms.city_id")
    city_id: Mapped[int | None] = mapped_column(ForeignKey("cities.id"), nullable=True)