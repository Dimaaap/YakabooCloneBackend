from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .gifts import Gift


class GiftSeries(Base):
    __tablename__ = "gift_series"

    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True)

    gifts: Mapped[list["Gift"]] = relationship("Gift", back_populates="seria",
                                               cascade="all, delete-orphan", uselist=False)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(title={self.title}, slug={self.slug})"