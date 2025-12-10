from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, Integer, ForeignKey, Index, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .city import City
    from .order import Order


class MeestPostOffice(Base):
    __tablename__ = "meest_post_offices"

    __table_args__ = (
        Index("idx_meest_active", "id",
              postgresql_where=text("active = true")
        ),

        Index("idx_meest_city_active",
              "city_id", "id",
              postgresql_where=text("active = true")
        )
    )

    office_number: Mapped[int] = mapped_column(Integer)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    city: Mapped["City"] = relationship(back_populates="meest_post_offices",
                                        uselist=False,
                                        foreign_keys="MeestPostOffice.city_id")
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=False)

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="meest_office",cascade="all, delete-orphan")

    def __str__(self):
        return f"{self.__class__.__name__}(№={self.office_number}, address={self.address})"