from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey

from .base import Base


class HobbyAgesAssociation(Base):
    __tablename__ = "hobby_ages_association"

    hobby_id: Mapped[int] = mapped_column(ForeignKey("hobbies.id"), primary_key=True)
    board_game_age_id: Mapped[int] = mapped_column(ForeignKey("board_game_ages.id"), primary_key=True)
