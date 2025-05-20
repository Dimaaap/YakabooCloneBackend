import enum
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .board_games import BoardGame


class Theme(enum.Enum):
    NATURE = "Природа, пейзажі"
    VEHICLES = "Авто-мото, техніка"
    ARCHITECTURE = "Архітектура"
    COUNTRIES_AND_CITIES = "Міста і країни"
    ART = "Мистецтво"
    MOVIES_AND_CARTOONS = "Фільми і мультфільми"
    SHIPS = "Кораблі"
    EDUCATIONAL = "Навчальні"
    PEOPLE = "Люди"
    FANTASY = "Фентезі"


class BoardLanguages(enum.Enum):
    UKRAINIAN = "Українська"
    RUSSIAN = "Російська"
    ENGLISH = "Англійська"
    FRENCH = "Французька"
    GERMAN = "Німецька"
    CZECH = "Чеська"
    SLOVAKIAN = "Словацька"
    SPANISH = "Іспанська"
    ROMANIAN = "Румунська"
    POLISH = "Польська"
    HUNGARIAN = "Угорська"


class BoardGameInfo(Base):
    __tablename__ = "board_game_info"

    description: Mapped[str] = mapped_column(Text)
    article: Mapped[str] = mapped_column(String(30), unique=True)
    package_size: Mapped[str] = mapped_column(String(30), server_default="", default="")
    weight: Mapped[int] = mapped_column(Integer, nullable=True)

    theme: Mapped[Theme] = mapped_column(
        Enum(Theme, name="theme"), nullable=True
    )

    language: Mapped[BoardLanguages] = mapped_column(
        Enum(BoardLanguages, name="language"), default=BoardLanguages.UKRAINIAN,
        server_default=BoardLanguages.UKRAINIAN.name
    )

    board_game: Mapped["BoardGame"] = relationship("BoardGame", back_populates="board_game_info", uselist=False)





