from typing import TYPE_CHECKING

from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .hobby import Hobby


class HobbyCategory(Base):
    __tablename__ = "hobby_categories"

    title: Mapped[str] = mapped_column(String(50))
    slug: Mapped[str] = mapped_column(String(55), unique=True)
    images_src: Mapped[list[str]] = mapped_column(JSON, nullable=True)

    hobbies: Mapped[list["Hobby"]] = relationship("Hobby", back_populates="category", cascade="all, delete-orphan")
