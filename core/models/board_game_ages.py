import enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Enum, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base

if TYPE_CHECKING:
    from .board_games import BoardGame


class Age(enum.Enum):
    TEENAGERS = "Підліткам"
    FROM_9_TO_12 = "Від 9 до 12 років"
    FROM_6_TO_8 = "Від 6 до 8 років"
    FROM_3_TO_5 = "Від 3 до 5 років"
    PARENTS = "Батькам"
    TO_2_YEARS = "До 2-х років"


class BoardGameAge(Base):
    __tablename__ = "board_game_ages"

    board_game_code: Mapped[int] = mapped_column(ForeignKey("board_games.code"))
    age: Mapped[Age] = mapped_column(Enum(Age, name="age_enum"))

    board_games: Mapped["BoardGame"] = relationship(back_populates="ages")