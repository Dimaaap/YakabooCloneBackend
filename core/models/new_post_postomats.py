from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, Integer, ForeignKey, Index, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .city import City
    from .order import Order


class NewPostPostomat(Base):
    __tablename__ = 'new_post_postomats'

    __table_args__ = (
        Index("idx_new_post_postomat_active",
              "id",
              postgresql_where=text("active = true")
        ),

        Index("idx_new_postomat_city_active",
              "city_id",
              "id",
              postgresql_where=text("active = true")
        )
    )

    number: Mapped[int] = mapped_column(Integer, unique=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    city: Mapped["City"] = relationship(back_populates="new_post_postomats",
                                        uselist=False,
                                        foreign_keys = "NewPostPostomat.city_id")
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=False)

    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="new_post_postomat",
        cascade="all, delete-orphan"
    )

    def __str__(self):
        return f"{self.__class__.__name__}(number={self.number}, address={self.address})"