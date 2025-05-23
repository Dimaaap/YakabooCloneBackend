from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey

from .base import Base


class BoardGameAgeAssociation(Base):
    __tablename__ = "board_game_age_association"

    board_game_id: Mapped[int] = mapped_column(ForeignKey("board_games.code"))
    age_id: Mapped[int] = mapped_column(ForeignKey("board_game_ages.id"))