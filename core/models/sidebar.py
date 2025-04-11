from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Sidebar(Base):
    title: Mapped[str] = mapped_column(String(100), unique=True)
    slug: Mapped[str] = mapped_column(String(110), unique=True)
    icon: Mapped[str] = mapped_column(String(255), default="", server_default="")
    visible: Mapped[bool] = mapped_column(Boolean, server_default="1", default=True)
    order_number: Mapped[int] = mapped_column(Integer, server_default="1", default=1)
    is_clickable: Mapped[bool] = mapped_column(Boolean, server_default="0", default=0)

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, title={self.title}, slug={self.slug}, "
                f"is_visible={self.visible}")
