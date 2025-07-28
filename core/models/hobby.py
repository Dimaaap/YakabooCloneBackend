from typing import TYPE_CHECKING

from sqlalchemy import String, Text, Enum as SQLEnum, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .book_info import BookLanguages

from .base import Base

if TYPE_CHECKING:
    from .board_game_ages import BoardGameAge
    from .hobby_brands import HobbyBrand
    from .hobby_game_series import HobbyGameSeries
    from .hobby_image import HobbyImage


class Hobby(Base):
    __tablename__ = 'hobbies'

    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    image: Mapped[str] = mapped_column(Text, default="", server_default="")
    article: Mapped[str] = mapped_column(String(10), unique=True)
    size: Mapped[str] = mapped_column(String(18), default="", server_default="")
    language: Mapped[BookLanguages] = mapped_column(SQLEnum(BookLanguages), default=BookLanguages.UKRAINIAN,
                                                    server_default=BookLanguages.UKRAINIAN.name)
    weight: Mapped[int] = mapped_column(Integer, nullable=True, default=None)
    code: Mapped[int] = mapped_column(Integer, unique=True)
    details_count: Mapped[int] = mapped_column(Integer, nullable=True)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    ages: Mapped[list["BoardGameAge"]] = relationship(
        secondary="hobby_ages_association",
        back_populates="hobbies",
    )

    brand_id: Mapped[int] = mapped_column(ForeignKey("hobby_brands.id"))
    brand: Mapped["HobbyBrand"] = relationship("HobbyBrand", back_populates="hobbies")

    seria_id: Mapped[int] = mapped_column(ForeignKey("hobby_game_series.id"), nullable=True)
    seria: Mapped["HobbyGameSeries"] = relationship("HobbyGameSeries", back_populates="hobbies")

    images: Mapped[list["HobbyImage"]] = relationship(
        back_populates="hobby",
        cascade="all, delete-orphan",
        lazy="selectin",
    )