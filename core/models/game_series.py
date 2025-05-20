from typing import TYPE_CHECKING

from sqlalchemy import String, Text, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .board_games import BoardGame


class GameSeries(Base):
    __tablename__ = "game_series"

    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255))

    board_games: Mapped[list["BoardGame"]] = relationship("BoardGame",
                                                          back_populates="seria",
                                                          cascade="all, delete-orphan")

    def __str__(self):
        return f"{self.__class__.__name__}(title={self.title}, slug={self.slug})"