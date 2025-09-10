from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey

from .base import Base


class GiftAgeAssociation(Base):
    __tablename__ = "gift_ages_association"

    gift_id: Mapped[int] = mapped_column(ForeignKey("gifts.id"), primary_key=True)
    board_game_age_id: Mapped[int] = mapped_column(ForeignKey("board_game_ages.id"), primary_key=True)