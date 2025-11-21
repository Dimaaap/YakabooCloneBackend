from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .countries import Country
    from .delivery_terms import DeliveryTerms
    from .payment_methods import PaymentMethod
    from .ukrpost_office import UkrpostOffice


class City(Base):
    __tablename__ = "cities"

    title: Mapped[str] = mapped_column(String(150))
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    region: Mapped[str] = mapped_column(String(255))

    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))
    country: Mapped["Country"] = relationship(back_populates="cities")
    delivery_terms: Mapped["DeliveryTerms"] = relationship(
        back_populates="city",
        uselist=False,
        cascade="all, delete-orphan"
    )

    ukrpost_offices: Mapped["UkrpostOffice"] = relationship(
        back_populates="city",
        uselist=False,
        cascade="all, delete-orphan"
    )

    payment_methods: Mapped["PaymentMethod"] = relationship(
        back_populates="city",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __str__(self):
        return f"{self.__class__.__name__}(title={self.title})"

