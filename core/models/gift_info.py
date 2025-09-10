import enum
from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, Enum, Integer, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .gifts import Gift


class GiftThemeEnum(enum.Enum):
    FAMOUS_PEOPLE = "Відомі люди і персонажі. Література"
    OTHER = "Інші"
    ANIMALS = "Тварини"
    LITERATURE = "Література"


class GiftLanguagesEnum(enum.Enum):
    UKRAINIAN = "Українська"
    ENGLISH = "Англійська"
    SPANISH = "Іспанська"
    POLISH = "Польська"
    FRANCE = "Французька"
    GERMAN = "Німецька"


class GiftEventEnum(enum.Enum):
    OTHER = "Інше"
    ALL_CASES = "На всі випадки життя"


class GiftTypeEnum(enum.Enum):
    BAG = "Пакети"
    CERTIFICATE = "Подарунковий сертифікат"
    MARKS = "Листівки"


class GiftInfo(Base):
    __tablename__ = "gift_info"

    in_stock: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    visible: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    code: Mapped[int] = mapped_column(Integer, unique=True)
    rate: Mapped[float] = mapped_column(Float, nullable=True)
    ISBN: Mapped[str] = mapped_column(String(50), unique=True)
    bonuses: Mapped[int] = mapped_column(Integer, nullable=True)

    is_has_esupport: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    is_has_cashback: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")

    pages_count: Mapped[int] = mapped_column(Integer, nullable=True)
    item_size: Mapped[str] = mapped_column(String(20), nullable=True)
    packing_size: Mapped[str] = mapped_column(String(20), nullable=True)
    illustrations: Mapped[str] = mapped_column(String(30), nullable=True)
    packing_type: Mapped[str] = mapped_column(String(40), nullable=True)
    cover_type: Mapped[str] = mapped_column(String(40), nullable=True)

    colors: Mapped[str] = mapped_column(String(150), nullable=True)
    weight: Mapped[int] = mapped_column(Integer, nullable=True)
    publishing_year: Mapped[int] = mapped_column(Integer, nullable=True)

    description: Mapped[str] = mapped_column(Text, nullable=True)


    language: Mapped[GiftLanguagesEnum] = mapped_column(
        Enum(GiftLanguagesEnum, name="gift_languages", create_type=True),
        default=GiftLanguagesEnum.UKRAINIAN, server_default=GiftLanguagesEnum.UKRAINIAN.name
    )
    gift_type: Mapped[GiftTypeEnum] = mapped_column(
        Enum(GiftTypeEnum, name="gift_type", create_type=True),
        nullable=True
    )

    theme: Mapped[GiftThemeEnum] = mapped_column(
        Enum(GiftThemeEnum, name="gift_theme", create_type=True),
        nullable=True
    )

    event: Mapped[GiftEventEnum] = mapped_column(
        Enum(GiftEventEnum, name="gift_event", create_type=True),
        nullable=True
    )

    gift: Mapped["Gift"] = relationship("Gift", back_populates="gift_info", uselist=False)

    def __str__(self):
        return f"{self.__class__.__name__}(ISBN={self.ISBN}, description={self.description})"




