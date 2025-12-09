from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .city import City
    from .order import Order


class NewPostOffice(Base):
    __tablename__ = "new_post_offices"

    number: Mapped[int] = mapped_column(Integer)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    weight_to: Mapped[int] = mapped_column(Integer, nullable=True)

    city: Mapped["City"] = relationship(back_populates="new_post_offices",
                                        uselist=False,
                                        foreign_keys="NewPostOffice.city_id")
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=False)

    orders: Mapped[list["Order"]] = relationship(
        back_populates="new_post_office",
        cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(number={self.number}, address={self.address})"