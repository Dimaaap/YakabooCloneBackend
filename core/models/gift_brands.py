from typing import TYPE_CHECKING

from sqlalchemy import String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .gifts import Gift


class GiftBrand(Base):
    __tablename__ = "gift_brands"

    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True)
    image: Mapped[str] = mapped_column(Text, default="", server_default="")
    description: Mapped[str] = mapped_column(Text, default="")
    visible: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    gifts: Mapped[list["Gift"]] = relationship("Gift",
                                               back_populates="brand",
                                               cascade="all, delete-orphan")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(title={self.title}, slug={self.slug})"

