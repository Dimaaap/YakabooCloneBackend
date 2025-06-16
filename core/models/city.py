from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .countries import Country


class City(Base):
    __tablename__ = "cities"

    title: Mapped[str] = mapped_column(String(150))
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    region: Mapped[str] = mapped_column(String(255))

    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))
    country: Mapped["Country"] = relationship(back_populates="cities")
