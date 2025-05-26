import enum
from typing import TYPE_CHECKING

from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base

if TYPE_CHECKING:
    from .board_games import BoardGame


class BoardSubcategories(str, enum.Enum):
    BOARD = "Настільні ігри"
    PUZZLE = "Пазли"
    CONUNDRUM = "Головоломки"


class BoardGameSubcategory(Base):
    __tablename__ = "board_game_subcategories"

    title: Mapped[BoardSubcategories] = mapped_column(Enum(BoardSubcategories,
                                                           name="subcategories_enum",
                                                           values_callable=lambda enum_cls: [e.value for e in enum_cls]))
    slug: Mapped[str] = mapped_column(String(255), unique=True)
    board_games: Mapped[list["BoardGame"]] = relationship("BoardGame",
                                                          back_populates="subcategory",
                                                          cascade="all, delete-orphan")

    def __str__(self):
        return f"{self.__class__.__name__}(title={self.title}, slug={self.slug})"