from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Contacts(Base):
    __tablename__ = "contacts"

    social_title: Mapped[str] = mapped_column(String(150), unique=True)
    link: Mapped[str] = mapped_column(String(255), default="", server_default="")
    icon_title: Mapped[str] = mapped_column(String(100), default="", server_default="")

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    def __str__(self):
        return f"{ self.__class__.__name__ }(title={self.social_title}, icon={self.icon_title})"
