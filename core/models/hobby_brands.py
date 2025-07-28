from typing import TYPE_CHECKING

from sqlalchemy import String, Text, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .hobby import Hobby


class HobbyBrand(Base):
    __tablename__ = "hobby_brands"

    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255))
    image: Mapped[str] = mapped_column(Text, default="", server_default="")
    description: Mapped[str] = mapped_column(Text, default="", server_default="")
    visible: Mapped[bool] = mapped_column(Boolean, server_default="1", default=True)

    hobbies: Mapped[list["Hobby"]] = relationship("Hobby",
                                                  back_populates="brand",
                                                  cascade="all, delete-orphan")


    def __str__(self):
        return f"{self.__class__.__name__}(title={self.title}, slug={self.slug})"