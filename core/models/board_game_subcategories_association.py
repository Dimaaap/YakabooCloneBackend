from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey

from .base import Base


class BoardGameSubcategoryAssociation(Base):
    __tablename__ = "board_game_subcategory_association"

    board_game_id: Mapped[int] = mapped_column(ForeignKey("board_games.code"))
    subcategory_id: Mapped[int] = mapped_column(ForeignKey("board_game_subcategories.id"))
