from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Banner(Base):
    image_src: Mapped[str] = mapped_column(String(255), default="", server_default="")
    visible: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    link: Mapped[str] = mapped_column(String(255), default="", server_default="")
    in_all_books_page: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    is_new_books_banner: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")

    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, visible={self.visible}, link={self.link})"