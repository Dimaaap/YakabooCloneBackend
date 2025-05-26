import enum
from typing import TYPE_CHECKING

from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base

if TYPE_CHECKING:
    from .board_games import BoardGame


class Age(str, enum.Enum):
    TEENAGERS = "Підліткам"
    FROM_9_TO_12 = "Від 9 до 12 років"
    FROM_6_TO_8 = "Від 6 до 8 років"
    FROM_3_TO_5 = "Від 3 до 5 років"
    PARENTS = "Батькам"
    TO_2_YEARS = "До 2-х років"


class BoardGameAge(Base):
    __tablename__ = "board_game_ages"

    age: Mapped[Age] = mapped_column(Enum(Age,
                                          name="age_enum",
                                          values_callable=lambda enum_cls: [e.value for e in enum_cls]))
    slug: Mapped[str] = mapped_column(String(255), unique=True)

    board_game: Mapped[list["BoardGame"]] = relationship(back_populates="ages",
                                                         secondary="board_game_age_association")
