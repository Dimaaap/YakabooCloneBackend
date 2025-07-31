import enum

from sqlalchemy import String, Boolean, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class FooterCategory(enum.Enum):
    YAKABOO = "Yakaboo"
    INFO = "Інформація"


class Footer(Base):

    title: Mapped[str] = mapped_column(String(100), unique=True)
    link: Mapped[str] = mapped_column(String, default="", server_default="")
    category: Mapped[FooterCategory] = mapped_column(SqlEnum(FooterCategory, name="footer_category_enum",
                                                             create_constraint=True),
                                                     default=FooterCategory.YAKABOO,
                                                     server_default=FooterCategory.YAKABOO.name)
    active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    def __str__(self):
        return f"{self.__class__.__name__}(self.title={self.title})"