import enum
from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, Date, Text, Integer, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .board_game_ages import BoardGameAge
    from .board_game_brands import BoardGameBrand
    from .game_series import GameSeries
    from .board_game_info import BoardGameInfo
    from .board_game_subcategories import BoardSubcategories


class Filters(enum.Enum):
    DISCOUNT = "Знижка"
    HIT = "Хіти продажу"


class Status(enum.Enum):
    IN_STOCK = "У наявності"
    READY = "Готові до відправки"


class Type(enum.Enum):
    FOR_FAMILY = "Сімейні"
    DEVELOPMENT = "Розвиваючі"
    CARD = "Карткові"
    FOR_PARTY = "Для вечірки"
    LOGICAL = "Логічні"
    ECONOMICAL = "Економічні"
    AGILITY = "На спритність"
    WALKING = "Ходилки"
    GAMBLING = "Азартні"
    ROMANTIC = "Романтичні"
    ROLE = "Рольові"
    FOR_OFFICE = "Для офісу"


class Kind(enum.Enum):
    GUESS_WHO = "Guess Who?"
    CLUEDO = "Cluedo"
    FUNNY = "Веселі"
    STRATEGIC = "Стратегічні"
    STUDY = "Навчальні"
    INTELLECTUAL = "Інтелектуальні"
    ACTIVE = "Активні"
    MONOPOLY = "Монополія"
    ROAD = "Дорожні"
    MILITARY = "Військові"
    LOTO = "Лото"
    DJENGA = "Дженга"
    DOMINO = "Доміно"
    SETS = "Набори"
    TWISTER = "Твістер"
    CHESS = "Шахи"
    EXPLAIN_WORD = "Поясни слово"
    MAFIA = "Мафія"
    DIXIT = "Dixit"
    ERUDITE = "Ерудит"
    BACKGAMMON = "Нарди"
    SOCCER = "Футбол"
    CROCODILE = "Крокодил"
    CAPITALIST = "Капіталіст"
    UNO = "UNO"
    MAZE = "Лабіринт"
    SEA_FIGHT = "Морський бій"
    FARM = "Ферма"
    SCRABBLE = "Scrabble"
    TREASURE_ISLAND = "Острів скарбів"
    CHECKERS = "Шашки"
    FIXIKS = "Фіксики"
    TIK_TOE_BOOM = "Тік так бум"
    HOCKEY = "Хокей"
    BILLIARDS = "Більярд"
    MANCHKIN = "Манчкін"
    POKER = "Набори для покеру"
    IMAGINARIUM = "Imaginarium"
    CASINO = "Казино"
    EVOLUTION = "Еволюція"
    ABALON = "Абалон"


class PlayersCount(enum.Enum):
    FROM_2_TO_16 = "Від 2 до 16"
    SOLO = "Для 1-го"
    FOR_TWO = "Для 2-х"
    FROM_2_TO_4 = "Від 2 до 4"
    FROM_2_TO_5 = "Від 2 до 5"
    FROM_1_TO_8 = "Від 1 до 8"
    FROM_3_TO_16 = "Від 3 до 16"
    FROM_3_TO_12 = "Від 3 до 12"
    FROM_4_TO_16 = "Від 4 до 16"
    FROM_7 = "Від 7-ми"
    FROM_2_TO_6 = "Від 2 до 6"
    FROM_3_TO_8 = "Від 3 до 8"


class BoardGame(Base):
    __tablename__ = "board_games"

    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255))
    image: Mapped[str] = mapped_column(Text, default="", server_default="")
    code: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    price: Mapped[int] = mapped_column(Integer)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    board_game_info: Mapped["BoardGameInfo"] = relationship("BoardGameInfo", back_populates="board_game")

    filters: Mapped[Filters | None] = mapped_column(
        Enum(Filters, name="filter"), nullable=True
    )

    status: Mapped[Status] = mapped_column(
        Enum(Status, name="status"), default=Status.IN_STOCK,
        server_default=Status.IN_STOCK.name
    )

    type: Mapped[Type] = mapped_column(
        Enum(Type, name="type"), nullable=True
    )

    kind: Mapped[Kind] = mapped_column(
        Enum(Kind, name="kind"), nullable=True
    )

    players_count: Mapped[PlayersCount] = mapped_column(
        Enum(PlayersCount, name="players_count"), nullable=True
    )

    ages: Mapped[list["BoardGameAge"]] = relationship(back_populates="board_game",
                                                      secondary="board_game_age_association")

    subcategories: Mapped[list["BoardSubcategories"]] = relationship(back_populates="board_games",
                                                                     secondary="board_game_subcategory_association")
    brand_id: Mapped[int] = mapped_column(ForeignKey("board_games_brands.id"), nullable=True)
    brand: Mapped["BoardGameBrand"] = relationship("BoardGameBrand", back_populates="board_games")
    seria_id: Mapped[int] = mapped_column(ForeignKey("game_series.id"), nullable=True)
    seria: Mapped["GameSeries"] = relationship("GameSeries", back_populates="board_games")

    def __str__(self):
        return f"{ self.__class__.__name__ }(title={self.title}, slug={self.slug}"