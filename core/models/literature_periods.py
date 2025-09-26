import enum
from typing import TYPE_CHECKING

from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .book import Book


class PeriodTitleType(str, enum.Enum):
    ANTIQUE = "Антична література. Стародавній світ"
    END_19_START_20 = "Література XIX - поч. XX ст. (до 1918 р)"
    FROM_17_TO_18 = "Література XVII - XVIII ст."
    WHOLE_20 = "Література XX ст."
    RENAISSANCE = "Середньовічна література. Відродження"
    MODERN = "Сучасна література"


class LiteraturePeriods(Base):
    __tablename__ = "literature_periods"

    title: Mapped[PeriodTitleType] = mapped_column(SQLEnum(PeriodTitleType, name="period_title_type_enum"),
                                                   nullable=False,
                                                   default=PeriodTitleType.MODERN,
                                                   server_default=PeriodTitleType.MODERN.name)
    slug: Mapped[str] = mapped_column(String(255), unique=True)
    books: Mapped[list["Book"]] = relationship(
        "Book", back_populates="literature_period",
        cascade="all, delete-orphan",
    )