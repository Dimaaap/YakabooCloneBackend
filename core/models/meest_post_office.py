from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .city import City


class MeestPostOffice(Base):
    __tablename__ = "meest_post_offices"

    office_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    city: Mapped["City"] = relationship(back_populates="meest_post_offices",
                                        uselist=False,
                                        foreign_keys="MeestPostOffice.city_id")
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=False)

    def __str__(self):
        return f"{self.__class__.__name__}(№={self.office_number}, address={self.address})"