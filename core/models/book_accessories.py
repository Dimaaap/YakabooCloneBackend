import enum
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Text, Boolean, Float, Enum as SQLEnum, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .accessories_images import AccessoriesImage
    from .accessouries_brand import AccessoriesBrand
    from .accessories_category import AccessoriesCategory


class AccessoryTheme(str, enum.Enum):
    CLASSIC = "Класична"
    FAMOUS_PEOPLE = "Відомі люди і песронажі"
    LITERATURE = "Література"


class AccessorySeria(str, enum.Enum):
    CAT_AND_DOG = "Кіт та собака",
    FAMOUS_PEOPLE = "Діячі"
    COURT_OF_THORNS = "Двір шипів та троянд"
    BAT_AND_KITTEN = "Кажан і кошеня"
    KYIV_NIGHT = "Ніч у Києві"
    ONCE_A_BROKEN_HEART = "Одного разу розбите серце"
    THRONE_OF_GLASS = "Трон зі скла"


class Events(str, enum.Enum):
    ALL_CASES = "На всі випадки життя"


class BookAccessories(Base):
    __tablename__ = "book_accessories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    slug: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[int] = mapped_column(Integer)
    image: Mapped[str] = mapped_column(Text, default="", server_default="")
    article: Mapped[str] = mapped_column(String(25), unique=True)
    size: Mapped[str] = mapped_column(String(15), default="", server_default="")
    code: Mapped[int] = mapped_column(Integer, unique=True)
    weight: Mapped[float] = mapped_column(Float, default=0.0, server_default="0.0", nullable=True)
    is_in_top: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    is_new: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    is_in_stock: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    bonuses: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    color: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=True)
    packing: Mapped[str] = mapped_column(String(100), nullable=True)
    event: Mapped[Events] = mapped_column(SQLEnum(Events,
                                                  name="accessories_events_enum",
                                                  values_callable=lambda x: [e.value for e in x]),
                                          nullable=True)
    type: Mapped[AccessoryTheme] = mapped_column(SQLEnum(AccessoryTheme,
                                                         name="accessories_types_enum",
                                                         values_callable=lambda x: [e.value for e in x]),
                                                 nullable=True)
    seria: Mapped[AccessorySeria] = mapped_column(SQLEnum(AccessorySeria,
                                                          name="accessories_seria_enum",
                                                          values_callable=lambda x: [e.value for e in x]),
                                                  nullable=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey("accessories_brands.id"), nullable=True)
    brand: Mapped["AccessoriesBrand"] = relationship("AccessoriesBrand", back_populates="accessories")

    category_id: Mapped[int] = mapped_column(ForeignKey("accessories_categories.id"), nullable=True)
    category: Mapped["AccessoriesCategory"] = relationship("AccessoriesCategory", back_populates="accessories")

    images: Mapped[list["AccessoriesImage"]] = relationship(
        back_populates="accessory",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

