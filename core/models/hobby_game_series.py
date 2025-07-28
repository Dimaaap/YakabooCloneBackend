from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .hobby import Hobby


class HobbyGameSeries(Base):
    __tablename__ = "hobby_game_series"

    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255))

    hobbies: Mapped[list["Hobby"]] = relationship("Hobby",
                                                    back_populates="seria",
                                                    cascade="all, delete-orphan")

    def __str__(self):
        return f"{self.__class__.__name__}(title={self.title}, slug={self.slug})"