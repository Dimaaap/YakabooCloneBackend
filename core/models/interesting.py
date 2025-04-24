from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Interesting(Base):
    __tablename__ = "interesting"

    title: Mapped[str] = mapped_column(String(100), default="", server_default="")
    slug: Mapped[str] = mapped_column(String(100), default="", server_default="")
    visible: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    def __str__(self):
        return f"{self.__class__.__name__}(self.title={self.title})"