from sqlalchemy import String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Knowledge(Base):
    title: Mapped[str] = mapped_column(String(100), default="", server_default="")
    slug: Mapped[str] = mapped_column(String(100), default="", server_default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    content: Mapped[str] = mapped_column(Text, default="", server_default="")

    def __str__(self):
        return f"{self.__class__.__name__}(title={self.title}, slug={self.slug}, is_active={self.is_active})"
