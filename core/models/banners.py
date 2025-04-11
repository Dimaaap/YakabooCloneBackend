from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Banner(Base):
    image_src: Mapped[str] = mapped_column(String(255), default="", server_default="")
    visible: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    link: Mapped[str] = mapped_column(String(255), default="", server_default="")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, visible={self.visible}, link={self.link})"