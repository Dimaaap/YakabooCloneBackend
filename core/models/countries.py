from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .city import City
    from .delivery_terms import DeliveryTerms


class Country(Base):
    __tablename__ = "countries"

    title: Mapped[str] = mapped_column(String(110), unique=True)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    cities: Mapped[list["City"]] = relationship(back_populates="country", cascade="all, delete-orphan")
    delivery_terms: Mapped["DeliveryTerms"] = relationship(
        back_populates="country",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __str__(self):
        return f"{self.__class__.__name__}(title={self.title})"